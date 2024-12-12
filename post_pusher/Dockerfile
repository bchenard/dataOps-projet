FROM python:3.9.20-slim-bookworm

RUN pip install kafka-python google-cloud-bigquery
ENV PYTHONUNBUFFERED=1

COPY ./service-account.json ./service-account.json
COPY ./post_pusher/ ./
CMD ["python", "main.py", "--kafka_host=kafka-broker-service:9092"]