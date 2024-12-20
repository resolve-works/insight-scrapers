
docker-build:
	docker build --tag insight-scrapers .

docker-run:
	docker run --env-file=.env insight-scrapers

asktheeu:
	set -a; source ./.env; poetry run python ./scrapers/asktheeu.py

nl_foia_covid:
	set -a; source ./.env; poetry run python ./scrapers/nl_foia_covid.py
