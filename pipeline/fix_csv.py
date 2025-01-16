import csv
import logging
import re
import os
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()])

def csv_time_column_fix(inputfile:str, outputfile:str):
    """
    Clean the Baby Tracker output csvs to remove comma in 'Time' column, and split the column into separate time and date columns
    Saves a new cleaned csv to the outputfile path
    :param inputfile: string path of input csv
    :param outputfile: string path of output csv
    """
    if not inputfile.endswith('.csv'):
        return logging.warning(f"{inputfile} is not a csv")

    with open(inputfile, mode='r', encoding='utf-8-sig') as file:
        csvFile = csv.DictReader(file)

        headers = csvFile.fieldnames + ['Date']

        # Write the modified data to the output CSV file
        with open(outputfile, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            logger.debug(f"{outfile} to be written to")
            for row in csvFile:
                try:
                    # Split Time:"dd/mm/yyyy, hh:mm" into Date:"dd/mm/yyyy" and Time:"hh:mm"
                    date_str = re.search(r"\d{2}\/\d{2}\/\d{4}", row['Time']).group()
                    time_str = re.search(r", (\d{2}:\d{2})", row['Time']).group(1)
                except Exception as e:
                    logger.warning(f"{e} in {inputfile}")
                row['Date'] = date_str
                row['timeonly'] = time_str

                # Replace previous time value with new time only value
                if 'Time' in row:
                    #del row['Time']
                    row['Time'] = row.pop('timeonly')

                writer.writerow(row)

def rename_csv_headers(inputfile:str, outputfile:str):
    """Rename the headers in a csv file in order to not have whitespace or brackets prior to import to the database"""
    if not inputfile.endswith('.csv'):
        return logging.warning(f"{inputfile} is not a csv")

    with open(inputfile, mode='r', encoding='utf-8-sig') as file:
        csvFile = csv.reader(file)

        rows = list(csvFile)

        headers = rows[0]
        newheaders = []
        for h in headers:
            h = h.lower()
            h = re.sub(r'[\(\)]', '', h)
            h = re.sub(r'\s', "_", h)
            h = h.replace("durationminutes", "duration_min")
            newheaders.append(h)

        rows[0] = newheaders

        with open(outputfile, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

def split_csv_into_days(inputfile:str, outputdir:str, maxdate:str = None):
    """
    Split the csv file into separate csvs, one per date. Files will be named yyyymmdd_<input file name>.
    :param inputfile: path to csv file to be split by date
    :param outputdir: directory where single date files will be written
    :param maxdate: optional parameter. If passed, function will only return files with a date greater than the param
                    must be a string in format yyyymmdd
    """
    if not inputfile.endswith('.csv'):
        return logging.warning(f"{inputfile} is not a csv")

    data_by_date = defaultdict(list)

    filename = os.path.basename(inputfile)

    with open(inputfile, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        headers = reader.fieldnames

        # Group each row by date
        if maxdate is not None: maxdate = datetime.strptime(maxdate, '%Y%m%d')
        for row in reader:
            date = row['date']
            if maxdate is not None:
                rowdate = datetime.strptime(date, '%d/%m/%Y')
                if rowdate > maxdate:
                    data_by_date[date].append(row)
            else:
                data_by_date[date].append(row)

    check_output_directory(outputdir)

    # Find each date and convert it to yyyymmdd in order to name each new file
    for date, rows in data_by_date.items():
        date = re.search(r"(\d{2})\/(\d{2})\/(\d{4})", date).groups()
        date = ''.join(reversed(date))
        outputfile = os.path.join(outputdir, '_'.join([date, filename]))

        # Write new split by date csvs to output directory
        with open(outputfile, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(rows)

def check_output_directory(output_directory:str):
    """Check if the output directory exists, and if it does not, create it.
        :param output_directory: string path to directory the cleaned data should go"""
    if not os.path.isdir(output_directory): os.mkdir(output_directory)

if __name__ == "__main__":
    inputdir = '../assets/data/'
    outputdir_staging = '../assets/data/staging/'
    outputdir_clean = '../assets/data/clean'
    check_output_directory(outputdir_staging)
    all_input_files = [f for f in os.listdir(inputdir)
                       if os.path.isfile(os.path.join(inputdir, f))
                       and os.path.splitext(f)[1] == '.csv']
    for f in all_input_files:
        csv_time_column_fix(os.path.join(inputdir,f), os.path.join(outputdir_staging,f))


    all_staged_files = [f for f in os.listdir(outputdir_staging)
                        if os.path.isfile(os.path.join(outputdir_staging, f))
                        and os.path.splitext(f)[1] == '.csv']
    for f in all_staged_files:
        rename_csv_headers(os.path.join(outputdir_staging, f), os.path.join(outputdir_staging, f))
        split_csv_into_days(os.path.join(outputdir_staging, f), outputdir_clean)
    logger.info(f"{','.join(all_staged_files)} cleaned and staged")