# define image source
FROM continuumio/miniconda3 as base

ENV DB_NAME=postgres
ENV DB_PASS=pw
ENV DB_USER=postgres
ENV DB_HOST=10.81.0.4

# mount code
VOLUME ["/app"]
WORKDIR /app
COPY . .

# run installation
RUN bash scripts/install.sh

# expose port -> will listen to this port
EXPOSE 8080

ENTRYPOINT ["bash", "scripts/start.sh"]