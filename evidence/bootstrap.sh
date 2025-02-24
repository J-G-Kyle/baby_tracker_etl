#!/bin/bash
set -e

echo "Initializing database and processing data"
python3 /baby_tracker_etl/pipeline/duckdb_setup.py
python3 /baby_tracker_etl/pipeline/fix_csv.py
python3 /baby_tracker_etl/pipeline/duckdb_import.py
python3 /baby_tracker_etl/pipeline/watchdog_etl.py &

echo "Starting Evidence.dev development environment mounted on $(pwd) in the container."
echo "Provided arguments => $@"

RUN_DEV_COMMAND="npm run sources && npm run dev -- --host 0.0.0.0"
COMMAND="npm install && $RUN_DEV_COMMAND"

case $1 in
    --init)
        echo "Starting with a blank template project."
        npx degit evidence-dev/template . && npm install
        if [ $# -gt 1 ];
        then
            COMMAND=${@:2}
        else
            COMMAND=$RUN_DEV_COMMAND
        fi
        ;;
    *)
        if [ $# -gt 0 ];
        then
            COMMAND=$@
        fi
        ;;
esac

echo "Running command => $COMMAND"
eval $COMMAND