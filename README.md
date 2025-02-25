## Baby Tracker ETL
This project is an ETL pipeline that takes csv files exported from the Baby Tracker app, cleans them, loads them 
into a DuckDB database, and then creates visualisations of the data in an Evidence.dev page at [localhost:3000](https://localhost:3000). 
It runs in a docker container for portability, using a mounted directory to allow for database persistence.

For an in-depth discussion of project background see my post on [Medium](https://medium.com/@jonathan.gordon.kyle/data-engineering-my-way-through-new-parenthood-3ed371c5e0be).

### Prequisites
Docker must be installed on your machine: [Docker Desktop Installation Instructions](https://docs.docker.com/desktop/)

### Get Started
1. Clone this repository in a directory of your choice
```
git clone https://github.com/J-G-Kyle/baby_tracker_etl
cd baby_tracker_etl
```

2.  Build and run the docker container
    1. If you have make installed
    ```
    make run docker-build
    make run docker-dev
    ```
    2. Otherwise, run from the start script
     ```
     chmod +x start_dev_container.sh
     ./start_dev_container.sh
     ```
3. Once the docker startup process is complete (~1 minute), go to [http://localhost:3000/](http://localhost:3000) to 
   see the results

### Adding newer data
Newly exported csv files from the Baby Tracker app with newer data can be added to `evidence/data`. The watchdog_etl 
python process will process the new files and write them to the database. Once the database has updated 
localhost:3000 can be refreshed and the new data will appear on the page.

### Add your own data
If you have your own csv files from the Baby Tracker app that you want to use instead, replace the files that are in ```evidence/data``` with your own exported csvs.

If you wish to use more tables that the ones in this project, change the config variable selected in duckdb_import.
py from "limitedtables" to "alltables", and create the appropriate new table.sql files in 
`evidence/sources/baby_tracker_data`.
