
build:
	docker build --tag asktheeu .

run-docker:
	docker run --env-file=.env asktheeu

run:
	set -a; source ./.env; python ./scrape.py
