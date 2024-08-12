FROM python:3.10
WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY .. /code/
EXPOSE 8000
