import os

import logging
import confluent_kafka
import json
import pymongo

mongodb_user = os.environ["MONGODB_ROOT_USER"]
mongodb_password = os.environ["MONGODB_ROOT_PASSWORD"]
mongodb_server = os.environ["MONGODB_SERVER"]
mongodb_db = os.environ["MONGODB_DATABASE"]
metadata_collection = os.environ["MONGODB_METADATA_TABLE"]

kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
images_bucket_event_topic = os.environ["IMAGES_BUCKET_EVENT_TOPIC"]
thumbnails_bucket_event_topic = os.environ["THUMBNAILS_EVENT_TOPIC"]

kafka_conf = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'group.id': 'indexer',
    'auto.offset.reset': 'earliest',
    'enable.partition.eof': 'false'
}

mongo_client = pymongo.MongoClient(
    "mongodb://{}:{}@{}".format(mongodb_user, mongodb_password, mongodb_server))
mongodb_db = mongo_client[mongodb_db]
metadata_collection = mongodb_db[metadata_collection]

# Create logger for consumer (logs will be emitted when poll() is called)
logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def launch():
    consumer = confluent_kafka.Consumer(kafka_conf, logger=logger)
    consumer.subscribe([images_bucket_event_topic])
    producer = confluent_kafka.Producer({'bootstrap.servers': kafka_bootstrap_servers})
    try:
        while True:
            msg = consumer.poll()
            if msg is None:
                continue
            if msg.error():
                raise confluent_kafka.KafkaException("Consumer error: {}".format(msg.error()))
            else:
                msg_json = json.loads(msg.value())
                x = metadata_collection.insert_one(msg_json["Records"][0])
                logger.info("ObjectID generated: {}".format(x.inserted_id))
                producer.poll(0)
                producer.produce(thumbnails_bucket_event_topic,
                                 json.dumps({"ObjectId": str(x.inserted_id)}).encode('utf-8'),
                                 callback=delivery_report)
                producer.flush()

    finally:
        consumer.close()


def main():
    """Launcher."""
    launch()


if __name__ == "__main__":
    main()
