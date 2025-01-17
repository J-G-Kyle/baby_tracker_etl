import duckdb
import logging
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def connect_to_baby_database() -> object:
    """Connect to the database using the connection path specified in the table_config.yaml file
    :return duckdb.con connection object"""
    with open("../assets/table_config.yaml", "r") as config_file:
        config_variables = yaml.safe_load(config_file)
        config_file.close()
    asher_database = config_variables["asher"]["database"]
    try:
        connection = duckdb.connect(asher_database)
        return connection
    except Exception as e:
        logger.warning(f"Connection to baby database failed: {e}")


if __name__ == "__main__":
    con = connect_to_baby_database()
    logger.info("Connected to database")

    con.sql("DROP SCHEMA IF EXISTS raw CASCADE;")
    con.sql("CREATE OR REPLACE SCHEMA raw;")
    con.sql("SET SCHEMA = 'raw';")

    # parse table config to get create table commands
    with open("../assets/table_config.yaml", "r") as f:
        table_config = yaml.safe_load(f)
        f.close()

    # create all tables in the raw schema using the table_config.yaml file
    for tablename in table_config["asher"]["alltables"]:
        con.sql(table_config["asher"][tablename])
        logger.info(f"Table raw.{tablename} created")
    con.close()
    logger.info("Database setup complete")
