VERSION=0.0.1
SHELL := /bin/bash
IMAGE_TAG=allergy:0.0.6

.PHONY: clean
clean :
	docker rm $$(docker ps -a -f status=exited -q)

.PHONY: build
build :
	docker build -t ${IMAGE_TAG} .

.PHONY: run
run :
	docker run -it \
		--mount src="$$(pwd)",target=/app,type=bind \
		--env HOST=0.0.0.0 \
		--env PORT=8080 \
		--env INSTANCE_CONNECTION_NAME=hackduke-2020-brohke:us-east1:hackduke-2020 \
		-p 8080:8080 \
		--entrypoint bash \
		 ${IMAGE_TAG} scripts/local_entrypoint.sh

.PHONY: fresh
fresh : clean build run

.PHONY: deploy
deploy :
	gcloud config set run/region us-east1 &&\
	 gcloud builds submit --tag gcr.io/hackduke-2020-brohke/${IMAGE_TAG} &&\
	 gcloud run deploy \
	    --image gcr.io/hackduke-2020-brohke/${IMAGE_TAG} \
	    --platform managed \
		--memory 1G \
		--add-cloudsql-instances hackduke-2020-brohke:us-east1:hackduke-2020 \
		--update-env-vars INSTANCE_CONNECTION_NAME="hackduke-2020-brohke:us-east1:hackduke-2020"