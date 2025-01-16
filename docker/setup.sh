# Usage notes: from baby_tracker_etl directory use docker buildx build .docker

# run required python scripts to set up database and import data
docker exec -it baby_tracker_container python3 app/pipeline/duckdb_setup.py
docker exec -it baby_tracker_container python3 app/pipeline/fix_csv.py
docker exec -it baby_tracker_container python3 app/pipeline/duckdb_import.py
docker exec -it baby_tracker_container python3 app/pipeline/watchdog_etl.py

# Create admin user.
docker exec -it baby_tracker_container superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin

# Upgrade database to latest.
docker exec -it baby_tracker_container superset db upgrade

# Setup roles.
docker exec -it baby_tracker_container superset init

# Create database connection for DuckDB.
docker exec -it baby_tracker_container superset set_database_uri \
    -d DuckDB-memory \
    -u duckdb:////assets/asher.duckdb