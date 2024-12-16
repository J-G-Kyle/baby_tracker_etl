# Usage notes: from baby_tracker_etl directory use docker buildx build .docker

# Create admin user.
docker exec -it baby_tracker_etl superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin

# Upgrade database to latest.
docker exec -it baby_tracker_etl superset db upgrade

# Setup roles.
docker exec -it baby_tracker_etl superset init

# Create database connection for DuckDB.
docker exec -it baby_tracker_etl superset set_database_uri \
    -d DuckDB-memory \
    -u duckdb:////Users/jonathankyle/PycharmProjects/baby_tracker_etl/assets/asher.duckdb