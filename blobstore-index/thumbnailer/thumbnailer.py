import glob
import os

from PIL import Image
from minio import Minio
from minio.error import ResponseError
import logging
import confluent_kafka
import pymongo
import json
from bson.objectid import ObjectId

minio_endpoint = os.environ["MINIO_ENDPOINT"]
minio_access_key = os.environ["MINIO_ACCESSKEY"]
minio_secret_key = os.environ["MINIO_SECRETKEY"]

minio_client = Minio(minio_endpoint,
                     minio_access_key,
                     minio_secret_key,
                     secure=False)

mongodb_user = os.environ["MONGODB_ROOT_USER"]
mongodb_password = os.environ["MONGODB_ROOT_PASSWORD"]
mongodb_server = os.environ["MONGODB_SERVER"]
mongodb_db = os.environ["MONGODB_DATABASE"]
metadata_collection = os.environ["MONGODB_METADATA_TABLE"]

kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
thumbnails_bucket_event_topic = os.environ["THUMBNAILS_EVENT_TOPIC"]

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


def start_consumer():
    conf = {
        'bootstrap.servers': kafka_bootstrap_servers,
        'group.id': 'thumbnailer',
        'auto.offset.reset': 'earliest',
        'enable.partition.eof': 'false'
    }

    consumer = confluent_kafka.Consumer(conf, logger=logger)

    consumer.subscribe([thumbnails_bucket_event_topic])
    try:
        while True:
            msg = consumer.poll()
            if msg is None:
                continue
            if msg.error():
                raise confluent_kafka.KafkaException("Consumer error: {}".format(msg.error()))
            else:
                object_id = json.loads(msg.value().decode('utf-8'))["ObjectId"]
                logger.info("ObjectId obtained: {}, extracting object bucket and key info ...".format(object_id))
                query_results = metadata_collection.find_one({"_id": ObjectId(object_id)},
                                                             {"s3.bucket.name": 1, "s3.object.key": 1, "_id": 0})
                local_image = download(query_results["s3"]["bucket"]["name"], query_results["s3"]["object"]["key"])
                thumbnail = generate_thumbnail(local_image)
                upload(thumbnail, "thumbnails", thumbnail)
                metadata_collection.update_one({"_id": ObjectId(object_id)},
                                               {"$set": {"thumbnails": "{}/{}".format("thumbnails", thumbnail)}})
    finally:
        consumer.close()


# Get a full object
def download(bucket, object_key):
    logger.info("Downloading image from {}/{}".format(bucket, object_key))
    try:
        data = minio_client.get_object(bucket, object_key)

        with open(os.path.split(object_key)[1], 'wb') as file_data:
            for d in data.stream(32 * 1024):
                file_data.write(d)
        return os.path.split(object_key)[1]
    except ResponseError as err:
        print(err)


def upload(local_file, bucket, object_key):
    logger.info("Uploading thumbnails for {} to {}/{}".format(local_file, bucket, object_key))
    try:
        with open(local_file, 'rb') as file_data:
            file_stat = os.stat(local_file)
            minio_client.put_object(bucket, object_key, file_data,
                                    file_stat.st_size, content_type='image/jpeg')
    except ResponseError as err:
        logger.error(err)
    finally:
        cleanup()


def generate_thumbnail(image_file):
    logger.info("Generating thumbnails for {}".format(image_file))
    size = 128, 128
    file_name, ext = os.path.splitext(image_file)
    im = Image.open(image_file)
    im.thumbnail(size)
    im.save(file_name + ".thumbnail", "JPEG")
    return file_name + ".thumbnail"


def cleanup():
    for file in glob.glob("*.thumbnail"):
        os.remove(file)
    for file in glob.glob("*.jpg"):
        os.remove(file)


def main():
    """Launcher."""
    # print("Downloading...")
    # local_image = download("images", "100501.jpg")
    # print("Generating thumbnail")
    # thumbnail = generate_thumbnail(local_image)
    # print("Uploading...")
    # upload(thumbnail, "thumbnails", thumbnail)
    start_consumer()


if __name__ == "__main__":
    main()
