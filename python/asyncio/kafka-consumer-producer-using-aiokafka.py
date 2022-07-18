"""
python3 -mvenv venv
venv/bin/pip install aiokafka
"""
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "my_topic"
GROUP_ID = "my_group"


async def start_consumer():
    consumer = AIOKafkaConsumer(
        TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID
    )
    await consumer.start()
    await consume_events(consumer)


async def consume_events(consumer):
    try:
        async for msg in consumer:
            print(
                f"topic - {msg.topic} | partition - {msg.partition} | offset - {msg.offset} | key - {msg.key} | "
                f"value - {msg.value} | timestamp - {msg.timestamp}"
            )
    finally:
        print("[*] stopping consumer...")
        await consumer.stop()


async def start_producer():
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    await producer.start()
    await produce_events(producer)


async def produce_events(producer, count=0):
    msg = "my msg %s" % count
    await producer.send_and_wait(TOPIC, msg.encode("utf-8"))
    if count < 10:
        await produce_events(producer, count=count + 1)
    else:
        print("[*] stopping producer...")
        await producer.stop()


def main():
    print("[*] starting consumer...")
    asyncio.create_task(start_consumer())

    print("[*] staring producer...")
    asyncio.create_task(start_producer())


loop = asyncio.get_event_loop()
loop.call_later(1, main)
loop.run_forever()
