services:
	docker-compose down
	docker-compose up -d

stop:
	docker-compose down

test-domain:
	coverage run -m test.test_domain

test-log:
	coverage run -m test.test_log

tests:
	make test-domain
	make test-log

lint:
	flake8 --exclude venv/ . --max-line-length=120
