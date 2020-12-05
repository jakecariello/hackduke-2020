# define image source
FROM continuumio/miniconda3 as base

# mount code
VOLUME ["/app"]
WORKDIR /app
COPY . .

# run installation
RUN bash scripts/install.sh

# expose port -> will listen to this port
EXPOSE 8080

ENTRYPOINT ["bash", "scripts/start.sh"]