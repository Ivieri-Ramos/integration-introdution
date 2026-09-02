run-shell:
	mkdir -p output
	chmod 777 output
	docker compose build
	docker compose run --rm -v "./output:/app/output" app main.py