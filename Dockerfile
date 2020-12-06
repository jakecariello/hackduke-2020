# define image source
FROM continuumio/miniconda3 as base

ENV DB_NAME=postgres
ENV DB_PASS=pw
ENV DB_USER=postgres
ENV DB_HOST=34.74.11.222

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# mount code
VOLUME ["/app"]
WORKDIR /app
COPY . .

# run installation
RUN bash scripts/install.sh

# expose port -> will listen to this port
EXPOSE 8080

ENTRYPOINT ["bash", "scripts/start.sh"]