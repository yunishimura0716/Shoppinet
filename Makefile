build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

test-backend:
	docker-compose run --rm backend sh -c "python3 manage.py test && flake8"

test-backend-ci:
	docker-compose -f .github/docker-compose-ci.yml run --rm backend sh -c "python3 manage.py test && flake8"

down-ci:
	docker-compose -f .github/docker-compose-ci.yml down
