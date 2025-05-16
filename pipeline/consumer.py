"""Module for consuming messages from a kafka cluster."""

from json import loads
import json
from os import environ as ENV
import logging
from datetime import datetime

from confluent_kafka import Consumer, Message
from dotenv import load_dotenv

from logger import get_logger


def get_consumer():
    """Return a consumer connected to a Kafka cluster defined in environment."""
    load_dotenv()

    config = {
        'bootstrap.servers': ENV["BOOTSTRAP_SERVERS"],
        "auto.offset.reset": ENV["AUTO_OFFSET"],
        'security.protocol': ENV["SECURITY_PROTOCOL"],
        'sasl.mechanisms': ENV["SASL_MECHANISM"],
        'sasl.username': ENV["KAFKA_USERNAME"],
        'sasl.password': ENV["KAFKA_PASSWORD"],
        'group.id': ENV["GROUP"]
    }

    return Consumer(config)


def is_valid_message(message: json) -> tuple[bool, str]:
    """Return (valid, error) for message."""
    keys = ['at', 'site', 'val']
    for k in keys:
        if message.get(k) is None:
            return (False, f"No key called '{k}'")

    at = message.get('at')
    if not isinstance(at, str):
        return (False, f"'at' value type is incorrect: {type(at)}")
    if not bool(datetime.fromisoformat(at)):
        return (False, f"'at' value is not in accepted format: {at}")
    site = message.get('site')
    if not site.isnumeric():
        return (False, f"'site' value type is incorrect: {type(site)}")
    if site not in ["0", "1", "2", "3", "4", "5"]:
        return (False, f"'site' value is not in accepted list of values: {site}")
    val = message.get('val')
    if not isinstance(val, int):
        return (False, f"'val' value type is incorrect: {type(val)}")
    if val not in [-1, 0, 1, 2, 3, 4]:
        return (False, f"'val' value is not in accepted list of values: {val}")

    if val == -1:
        mes_type = message.get('type')
        if mes_type is None:
            return (False, "No key called 'type'")
        if mes_type not in [0, 1]:
            return (False, f"'type' value type is incorrect: {type(mes_type)}")

    return (True, "Valid message.")


def log_message(message: Message):
    """Logs consumed messsages from kafka cluster."""
    logger = logging.getLogger("etl_logger")
    if message:
        val = message.value().decode()
        (valid, err) = is_valid_message(loads(val))
        if valid:
            logger.info("MESSAGE: %s", val)
        else:
            logger.error("INVALID: %s, with ERROR: %s", val, err)


def get_message_data(message: Message) -> list:
    """Return list formatted data from message."""
    logger = logging.getLogger("etl_logger")
    body = loads(message.value().decode())
    (valid, _) = is_valid_message(body)
    if valid:
        logger.info("Formatted message as list: %s", body)
        if body.get('val') != -1:
            return [body['at'], body['site'], body['val']]
        return [body['at'], body['site'], body['val'], body['type']]
    return None


if __name__ == "__main__":
    get_logger(False)
    cons = get_consumer()
    cons.subscribe(["lmnh"])
    while True:
        message = cons.poll(1.0)
        if message:
            log_message(message)
            print(get_message_data(message))
