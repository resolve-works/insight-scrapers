
docker-build:
	docker build --tag insight-scrapers .

docker-run:
	docker run --env-file=.env insight-scrapers

run:
	set -a; source ./.env; poetry run python ./scrape.py
