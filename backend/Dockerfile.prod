FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --proxy="http://wwwproxy.uni-muenster.de:3128" -r requirements.txt

COPY . .