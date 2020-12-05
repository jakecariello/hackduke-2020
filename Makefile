VERSION=0.0.1
REPO=recipespace
SHELL := /bin/bash

.PHONY: clean
clean :
	docker rm $$(docker ps -a -f status=exited -q)
	docker rmi recipespace:0.0.1

.PHONY: start
start :
	docker-compose -f docker/docker-compose.yml up

.PHONY: fresh
fresh : clean start