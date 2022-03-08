#Start the api server
api: createsuperuser
	docker compose run --rm api python manage.py migrate
	docker compose up

# Recreate the api docker image (used when changing the requirements)
rebuild:
	docker compose build api

# Start a terminal inside the api container for ease of development
shell:
	docker compose run --rm api /bin/bash

# This creates the superuser once, to run again remove the createsuperuser file
createsuperuser:
	docker compose run --rm api python manage.py migrate
	docker compose run --rm api python manage.py createsuperuser --no-input
	touch createsuperuser

# Delete local data to start all over again
purge:
	docker compose down
	docker volume rm -f bank_program_local_postgres_data
	rm createsuperuser

test:
	docker compose run --rm api pytest
