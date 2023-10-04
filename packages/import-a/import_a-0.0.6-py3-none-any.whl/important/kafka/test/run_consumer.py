import os

from confluent_kafka import Consumer


KAFKA_HOST = os.environ.get('KAFKA_HOST')
TOPIC_NAME = os.environ.get('TOPIC_NAME')
GROUP_ID = os.environ.get('GROUP_ID')
AUTO_OFFSET_RESET = os.environ.get('AUTO_OFFSET_RESET')
POLLING_TIMEOUT_SECS = os.environ.get('POLLING_TIMEOUT_SECS')


# Create Consumer instance
consumer = Consumer({"bootstrap.servers": KAFKA_HOST, 
                     "group.id": GROUP_ID,
                     'auto.offset.reset': AUTO_OFFSET_RESET})


# Subscribe to topic
consumer.subscribe([TOPIC_NAME])


# Poll for new messages from Kafka and print them.
try:
    while True:
        msg = consumer.poll(timeout=float(POLLING_TIMEOUT_SECS))
        if msg is None:
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            print("Waiting...")
        elif msg.error():
            print(msg.error())
            print("ERROR: %s".format(msg.error()))
        else:
            # Extract the (optional) key and value, and print.
            print("Consumed event from topic {topic}: key = {key:12} value = {value:12}" \
                  .format(topic=msg.topic(),
                          key=msg.key().decode('utf-8'),
                          value=msg.value().decode('utf-8')))
except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
