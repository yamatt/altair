# https://hub.docker.com/_/python
FROM python:3.12.2-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /
WORKDIR $APP_HOME
COPY requirements.lock ./src/altair ./

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

CMD ["uvicorn", "webhook:webhook", "--host", "0.0.0.0", "--port", "8080"]

