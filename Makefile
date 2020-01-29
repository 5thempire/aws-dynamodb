services:
	docker-compose down
	docker-compose up -d

test:
	python tests.py
