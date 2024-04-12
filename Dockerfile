FROM python:3.11-alpine

WORKDIR /app

RUN pip install --no-cache-dir influxdb

COPY . .

CMD [ "python", "./Loxone2InfluxDB.py" ]
