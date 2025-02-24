run:
	docker exec -i baby_tracker_container python3 /baby_tracker_etl/pipeline/duckdb_setup.py
	docker exec -i baby_tracker_container python3 /baby_tracker_etl/pipeline/fix_csv.py
	docker exec -i baby_tracker_container python3 /baby_tracker_etl/pipeline/duckdb_import.py
	docker exec -i baby_tracker_container bash -c "cd evidence && npm install"
	docker exec -i baby_tracker_container bash -c "cd evidence && npm run sources"
	docker exec -i baby_tracker_container python3 /baby_tracker_etl/pipeline/watchdog_etl.py 2>&1 &

dev:
	docker exec -i baby_tracker_container bash -c  "cd evidence && npm run dev -- --host 0.0.0.0" #&
	echo "Evidence started successfully, available at localhost:3000"

docker-build:
	docker buildx build -t baby_tracker_image_evidence -f Dockerfile .

docker-dev:
		docker run -d \
		--mount type=bind,source=/$(shell pwd)/evidence,target=/evidence \
		--publish 3000:3000 \
		--name baby_tracker_container \
		baby_tracker_image_evidence
		make run dev