POSTGRES_IMAGE ?= popug-todo-postgres:1.0

build_postgres:
	make -C tests/docker/postgres/ build

run_postgres: build_postgres
	docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=testpassword --name popugpg $(POSTGRES_IMAGE)