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

# create all tables in the raw schema using the table config file schemas
con.sql(table_config["asher"]["diaper"])
con.sql(table_config["asher"]["expressed"])
con.sql(table_config["asher"]["formula"])
con.sql(table_config["asher"]["growth"])
con.sql(table_config["asher"]["nursing"])
con.sql(table_config["asher"]["sleep"])
con.sql(table_config["asher"]["pump"])
con.sql(table_config["asher"]["milestone"])

# con.sql("DESCRIBE raw.diaper;").show()
# con.sql("SELECT * FROM raw.diaper LIMIT 10;").show()
# print(duckdb.read_csv('../data/Asher_diaper.csv', quotechar='"', header=True))

# con.sql("FROM sniff_csv('../data/Asher_diaper.csv');").show()

# con.sql("SELECT * FROM raw.expressed;").show()

# importfile = "../data/clean/20240905_Asher_diaper.csv"
# importsql = """COPY raw.nursing FROM read_csv('../data/clean/20240922_Asher_nursing.csv', quotechar='"', header=True);"""
# importsql = """COPY raw.nursing FROM '../data/clean/20240922_Asher_nursing.csv' (HEADER);"""
# con.sql(importsql)
# con.sql("SELECT * FROM nursing;").show()

con.close()