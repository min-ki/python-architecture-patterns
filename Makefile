test:
		pytest --tb=short

watch-tests:
		ls *.py | entr pytest --tb=short

black:
	black -l 86 $$(find * -name '*.py')

up:
		docker-compose up -d
		
e2e-tests: up
		docker-compose run --rm --no-deps --entrypoint=pytest api /tests/e2e
