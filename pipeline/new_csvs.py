import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from fix_csv import csv_time_column_fix, rename_csv_headers, split_csv_into_days
import duckdb_import
from duckdb_setup import connect_to_baby_database
from duckdb_import import check_table_exists

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    stream=sys.stdout,
)


def maximum_date_from_table(tablename: str) -> str:
    """
    Connect to the database and return the newest date in the selected table
    :param tablename the name of the required table in the raw schema
    :returns the maximum date in the table as a string in format yyyymmdd
    """
    database_connection = connect_to_baby_database()
    maxdate = database_connection.sql(
        f"SELECT MAX(date) FROM raw.{tablename};"
    ).fetchone()
    if maxdate[0] is None:
        maxdate = (datetime.min.date(),)
    # connect.sql.fetchone() returns a tuple object, of which the date is in datetime format
    maxdate = maxdate[0].isoformat()
    maxdate = str.replace(maxdate, "-", "")

    return maxdate


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.warning("No file name provided to new_csvs.py by watchdog_etl!")
    else:
        file_path = sys.argv[1]

    file_path = "/Users/jonathankyle/PycharmProjects/baby_tracker_etl/evidence/dataAsher_nursing2.csv"

    module_dir = Path(__file__).parent
    inputdir_relative_path = "/../../evidence/data/"
    inputdir = module_dir / inputdir_relative_path
    outputdir_staging_relative_path = "data/staging"
    outputdir_staging = module_dir / outputdir_staging_relative_path
    outputdir_clean_relative_path = "data/clean"
    outputdir_clean = module_dir / outputdir_clean_relative_path

    # get the file path from watchdog
    new_file_path = sys.argv[1]
    # get only the file name
    new_file_name = os.path.split(new_file_path)[1]

    # get the table name from the filename
    table_name = duckdb_import.find_table_name(new_file_name)

    # check the table exists, otherwise create it
    database_connection = connect_to_baby_database()
    check_table_exists("raw", table_name, database_connection)

    # find the date of the newest data in the table
    newestdata = maximum_date_from_table(table_name)

    # For each new file, fix the time columns, rename headers, and split into days where the date is greater than
    # the newest data in the table
    csv_time_column_fix(
        os.path.join(inputdir, new_file_name),
        os.path.join(outputdir_staging, new_file_name),
    )
    rename_csv_headers(
        os.path.join(outputdir_staging, new_file_name),
        os.path.join(outputdir_staging, new_file_name),
    )
    split_csv_into_days(
        os.path.join(outputdir_staging, new_file_name),
        str(outputdir_clean),
        newestdata,
    )

    # create a list of the newest files
    newest_files = [
        f
        for f in os.listdir(outputdir_clean)
        if os.path.isfile(os.path.join(outputdir_clean, f))
        and f.split("_", 1)[0] > newestdata
    ]

    # load them into duckDB
    if len(newest_files) == 0:
        logger.info("No new data imported")
    else:
        duckdb_import.import_csv_to_duckdb(
            newest_files, database_connection, str(outputdir_clean)
        )
        logger.info(f"All new data successfully imported from {new_file_path}")
        duckdb_import.cleanup_folder(str(outputdir_clean), newest_files)
        logger.info(f"{len(newest_files)} files removed from {outputdir_clean}")

    # refresh Evidence sources to update tables
    subprocess.run(
        "cd /evidence && npm run sources",
        shell=True,
        check=True,
        text=True,
    )
