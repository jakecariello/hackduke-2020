VERSION=0.0.1
SHELL := /bin/bash
IMAGE_TAG=allergy:0.0.3

.PHONY: clean
clean :
	docker rm $$(docker ps -a -f status=exited -q)
	docker rmi ${IMAGE_TAG}

.PHONY: build
build :
	docker build -t ${IMAGE_TAG} .

.PHONY: run
run :
	docker run --env HOST=0.0.0.0 --env PORT=8080 -p 8080:8080 ${IMAGE_TAG}

.PHONY: fresh
fresh : clean build run

.PHONY: deploy
deploy :
	gcloud config set run/region us-east1 &&\
	 gcloud builds submit --tag gcr.io/hackduke-2020-brohke/${IMAGE_TAG} &&\
	 gcloud run deploy --image gcr.io/hackduke-2020-brohke/${IMAGE_TAG} --platform managed --memory 1G