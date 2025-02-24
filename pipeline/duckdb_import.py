import os
import logging
from pathlib import Path
from duckdb_setup import connect_to_baby_database, get_config_variables

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def find_table_name(inputfile: str) -> str:
    """
    Get the table name that matches the type found in the csv file name
    :param inputfile: String filename
    :return: table name as written in the list if found in the input file
    """
    table_config = get_config_variables()

    tables = table_config["asher"]["limitedtables"]

    table = [table for table in tables if (table in inputfile)]
    if len(table) >= 1:
        return table[0]
    else:
        logger.warning(f"No matching table could be found for {inputfile}")


def check_table_exists(schema: str, table_name: str, database_connection: object):
    """
    Check if a table exists in database prior to import of data. If table does not exist, create it.
    This function is required to work around an error that occurs if a table exists with 0 rows.
    :param schema: String of schema where table is to be checked
    :param table_name: String of name of table
    :param database_connection: DuckDB connection object to database
    :return: True if table already exists, else create the table
    """
    # Returns a list of tuples containing information about every table in the database
    database_tables = database_connection.sql("SHOW ALL TABLES;").fetchall()

    # Get the list of tables in the format 'schema.table_name' from the database
    database_table_names = [".".join([table[1], table[2]]) for table in database_tables]

    qualified_table_name = ".".join([schema, table_name])

    if qualified_table_name in database_table_names:
        # No further action taken
        return True
    else:
        # Create table if it does not exist
        config_variables = get_config_variables()
        table_creation_sql = config_variables["asher"][table_name]
        database_connection.sql(f"SET SCHEMA = {schema};")

        database_connection.sql(table_creation_sql)
        logger.info(f"Table {schema}.{table_name} created.")


def import_csv_to_duckdb(
    input_files: list, database_connection: object, file_directory: str
):
    """
    Import a list of csv files to the matching table in duckDB
    :param input_files: List of all files to be imported
    :param database_connection: database connection object to the required database
    :param file_directory: String of the directory where the files are located
    :return: Logging warning if a file could not be imported
    """
    for f in input_files:
        table_name = find_table_name(f)
        filename = os.path.join(file_directory, f)
        if table_name is not None:
            try:
                database_connection.sql(
                    f"""COPY raw.{table_name} FROM '{filename}' (HEADER, DELIMITER ',');"""
                )
                logger.debug(f"File {f} successfully copied to table {table_name}")
            except Exception as e:
                logger.warning(f"{f} could not be copied to {table_name}")
                logger.exception(e)
        else:
            logger.warning(
                f"{filename} could not be imported - no matching table in duckdb"
            )


def cleanup_folder(input_directory: Path, input_files: list):
    """Cleanup the input_directory by deleting all csv files within it that are provided in input_files
    :param input_directory: path to directory to be cleaned
    :param input_files: list of all the files to be deleted from the directory"""
    for f in input_files:
        f_path = Path(os.path.join(input_directory, f))
        if os.path.isfile(f_path) and os.path.splitext(f_path)[1] == ".csv":
            try:
                Path.unlink(f_path)
            except Exception as e:
                logging.warning(f"Unable to remove file {f_path} due to error: {e}")


if __name__ == "__main__":
    module_dir = Path(__file__).parent
    outputdir_clean_relative_path = "data/clean"
    outputdir_clean = module_dir / outputdir_clean_relative_path
    con = connect_to_baby_database()

    all_input_files = [
        f
        for f in os.listdir(outputdir_clean)
        if os.path.isfile(os.path.join(outputdir_clean, f))
        and os.path.splitext(f)[1] == ".csv"
    ]
    try:
        import_csv_to_duckdb(all_input_files, con, outputdir_clean)

    except Exception as e:
        logging.warning(f"{e} in importing csv files to DuckDB")
    logger.info(
        f"{len(all_input_files)} files successfully imported from {outputdir_clean}"
    )
    # Cleanup cleaned data
    cleanup_folder(outputdir_clean, all_input_files)
    logger.info(f"{len(all_input_files)} files removed from {outputdir_clean}")
