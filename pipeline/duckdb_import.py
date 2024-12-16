import re
import os
import duckdb
import logging

def find_table_name(inputfile):

    table_name = re.search(r'_([a-z]*).csv', inputfile).groups()[0]
    return table_name
    # Use these as basis for pytest test
        # case "diaper": return "diaper"
        # case "expressed": return "expressed"
        # case "formula": return "formula"
        # case "growth": return "growth"
        # case "milestone": return "milestone"
        # case "nursing": return "nursing"
        # case "sleep": return "sleep"
        # case "pump": return "pump"
        # case _: return None

if __name__ == "__main__":
    inputdir = '../data/'
    outputdir_staging = '../data/staging/'
    outputdir_clean = '../data/clean'
    con = duckdb.connect("../assets/asher.duckdb")
    all_input_files = [f for f in os.listdir(outputdir_clean) if os.path.isfile(os.path.join(outputdir_clean, f))]
    for f in all_input_files:
        target_table = find_table_name(f)
        importfile = os.path.join(outputdir_clean, f)
        if target_table is not None:
            con.sql(f"""COPY raw.{target_table} FROM '{importfile}' (HEADER, DELIMITER ',');""")
        else: logging.warning(f"{importfile} could not be imported - no matching table in duckdb")