import os
import logging
import yaml
from pathlib import Path
from pipeline.duckdb_setup import connect_to_baby_database

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
    relative_path = Path("../assets/table_config.yaml")
    module_dir = Path(__file__).parent
    file_path = module_dir / relative_path
    with open(file_path, "r") as f:
        table_config = yaml.safe_load(f)
        f.close()

    tables = table_config["asher"]["alltables"]

    table = [table for table in tables if (table in inputfile)]
    if len(table) >= 1:
        return table[0]
    else:
        logger.warning(f"No matching table could be found for {inputfile}")


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


def cleanup_folder(input_directory: str, input_files: list):
    """Cleanup the input_directory by deleting all csv files within it that are provided in input_files
    :param input_directory: path to directory to be cleaned
    :param input_files: list of all the files to be deleted from the directory"""
    for f in input_files:
        f = os.path.join(os.path.join(input_directory, f))
        if os.path.isfile(f) and os.path.splitext(f)[1] == ".csv":
            try:
                Path.unlink(f)
            except Exception as e:
                logging.warning(e)


if __name__ == "__main__":

    outputdir_clean = "../assets/data/clean"
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
    cleanup_folder(outputdir_clean, all_input_files)
    logger.info(f"{len(all_input_files)} files removed from {outputdir_clean}")
