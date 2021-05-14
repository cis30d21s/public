from typing import Any
from gpiozero import LED
from signal import pause
from aws_iot_client import AwsIotClient
import os
import time
import pprint
from pathlib import PurePath
path = PurePath(os.path.dirname(__file__))

thing_name = 'cis30d21s-thing2'
broker_host = 'a16tjdo0hxywt6-ats.iot.us-west-2.amazonaws.com'
shadow_topic_prefix = f'$aws/things/{thing_name}/shadow'
led = LED(18)


def on_message(client: AwsIotClient, userdata: Any, message: Any, topic: str):
    if topic.endswith('/update/delta'):
        print('Update delta')
        pprint.pprint(message)
        led.on() if message['state']['led_on'] else led.off()
        update_status(bool(led.value), client)
    elif topic.endswith('/get/accepted'):
        print('Get response:')
        pprint.pprint(message)
        led.on() if message['state']['desired']['led_on'] else led.off()
    else:
        print(f'Not handled: topic={topic}, message={message}')


def update_status(led_on: bool, client: AwsIotClient):
    client.publish(shadow_topic_prefix + '/update', {
        "state": {
            "reported": {
                "led_on": led_on
            }
        }
    })


def main():
    client = AwsIotClient(
        broker_host, 443,
        root_ca=path/'AmazonRootCA1.pem',
        certfile=path/'thing2-cert.pem',
        keyfile=path/'thing2-priv.pem')
    client.subscribe([
        shadow_topic_prefix + '/get/accepted',
        shadow_topic_prefix + '/update/delta'],
        on_message)
    time.sleep(1)
    client.publish(shadow_topic_prefix + '/get')


if __name__ == '__main__':
    main()
    try:
        pause()
    except KeyboardInterrupt:
        ...
