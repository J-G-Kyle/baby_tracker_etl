import os
import duckdb
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def connect_to_baby_database() -> object:
    """Connect to the database using the connection path specified in the table_config.yaml file
    :return duckdb.con connection object"""
    config_variables = get_config_variables()
    asher_database_relative_path = Path(config_variables["asher"]["database"])
    module_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = str(module_dir / asher_database_relative_path)
    try:
        connection = duckdb.connect(file_path)
        return connection
    except Exception as e:
        logger.warning(f"Connection to baby database failed: {e}")
        exit()


def get_config_variables() -> object:
    relative_path = Path("../config/table_config.yaml")
    module_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = module_dir / relative_path
    with open(file_path, "r") as config_file:
        config_variables = yaml.safe_load(config_file)
        config_file.close()
    return config_variables


if __name__ == "__main__":
    con = connect_to_baby_database()
    logger.info("Connected to database")

    con.sql("DROP SCHEMA IF EXISTS raw CASCADE;")
    con.sql("CREATE OR REPLACE SCHEMA raw;")
    con.sql("SET SCHEMA = 'raw';")

    # Table creation now happens at data import due to database error involving tables that have 0 rows
    # This change prevents table creation from happening until data is imported to the table
    logger.info("Database setup complete")
