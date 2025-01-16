from token import ASYNC
import yaml
import duckdb
from duckdb.duckdb import read_csv

con = duckdb.connect("../assets/asher.duckdb")

con.sql("DROP SCHEMA IF EXISTS raw CASCADE;")

con.sql("CREATE OR REPLACE SCHEMA raw;")

con.sql("SET SCHEMA = 'raw';")

# parse table config to get create table commands
with open('../assets/table_config.yaml', 'r') as f:
    table_config = yaml.safe_load(f)
    f.close()

# create all tables in the raw schema using the table_config.yaml file
for tablename in table_config["asher"]["alltables"]:
    con.sql(table_config["asher"][tablename])

con.close()