# define image source
FROM continuumio/miniconda3 as base

# mount code
VOLUME ["/app"]
WORKDIR /app
COPY . .


RUN pip install pipenv
RUN pipenv install --deploy --system
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app