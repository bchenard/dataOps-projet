import logging
import random
import os
import json
from google.cloud import bigquery
import re
import time
import argparse
from kafka import KafkaProducer


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TOPIC = "posts"  # Name of the Kafka topic
SCHEMA = [  # Define the schema for the table
    bigquery.SchemaField('id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('post_type_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('accepted_answer_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('creation_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('score', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('view_count', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('body', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('owner_user_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('last_editor_user_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('last_edit_date', 'TIMESTAMP', mode='NULLABLE'),
    bigquery.SchemaField('last_activity_date', 'TIMESTAMP', mode='NULLABLE'),
    bigquery.SchemaField('title', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('tags', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('answer_count', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('comment_count', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('content_license', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('parent_id', 'STRING', mode='NULLABLE')
]

def transform_key(key):
    # Remove '@' and convert to snake_case
    key = key.replace('@', '')
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
    return key

def filter_post(post, allowed_columns):
    return {k: v for k, v in post.items() if k in allowed_columns}

def transform_and_filter_post(post, allowed_columns):
    transformed_post = {transform_key(k): v for k, v in post.items()}
    filtered_post = filter_post(transformed_post, allowed_columns)
    return filtered_post


def post_kafka(transformed_post, kafka_host):
    # Kafka configuration
    bootstrap_servers = [kafka_host]

    # Create Producer instance
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        # Produce and send a single message
        future = producer.send(TOPIC, transformed_post)
        record_metadata = future.get(timeout=10)
        print(f"Message delivered to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
    except Exception as e:
        print(f"Message delivery failed: {e}")
    finally:
        producer.close()

def main(multiple, kafka_host):
    # Load the post from the JSON file
    data_filepath = "./data/movies-stackexchange/json/posts.json"
    log.info(data_filepath)
    log.info(os.getcwd())
    with open(data_filepath, "r") as f:
        content = f.read()
    posts = json.loads(content)

    while True:
        post = random.choice(posts)

        allowed_columns = {field.name for field in SCHEMA}
        # Transform the post for insertion and save to a temporary JSON file
        transformed_post = transform_and_filter_post(post, allowed_columns)
        
        post_kafka(transformed_post, kafka_host)

        if not args.multiple:
            break

        time.sleep(10)

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--multiple', action='store_true', help='Send one message and exit')
    parser.add_argument('--kafka_host', type=str, required=True, default=None, help='The Kafka host address, changing BigQuery target to Kafka')
    args = parser.parse_args()

    main(
        multiple=args.multiple,
        kafka_host=args.kafka_host
    )