# $ python3 -m pip install paho-mqtt
from typing import Any, Callable, Optional
import paho.mqtt.client as mqtt
import ssl
import json
import os
import signal

OnConnectCallback = Callable[[mqtt.Client, Any, 'dict[str, int]', int], None]
OnMessageCallback = Callable[['AwsIotClient', Any, Any, str], None]


class AwsIotClient:
    def __init__(self, broker_host: str,
                 broker_port: int,
                 root_ca: 'os.PathLike[str]',
                 certfile: 'os.PathLike[str]',
                 keyfile: 'os.PathLike[str]',
                 on_connect: Optional[OnConnectCallback] = None):
        self._client = mqtt.Client()
        self._client.tls_set_context(
            self._ssl_alpn(root_ca, certfile, keyfile))
        self._client.on_connect = on_connect
        self._client.connect(broker_host, broker_port)
        self._client.loop_start()

    def publish(self, topic: str, message: Any = {}):
        message = json.dumps(message)
        result = self._client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"Sent `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def subscribe(self, topics: 'list[str]', on_message: OnMessageCallback):
        self._client.on_message = lambda client, userdata, message: on_message(
            self, userdata, json.loads(
                getattr(message, 'payload').decode('utf-8')), message.topic)
        original_on_connect = self._client.on_connect

        def on_connect(client: mqtt.Client, userdata: Any, flags: 'dict[str, int]', rc: int):
            if original_on_connect:
                original_on_connect(client, userdata, flags, rc)
            self._client.subscribe([(topic, 0) for topic in topics])
        self._client.on_connect = on_connect

    def stop(self):
        self._client.loop_stop()
        self._client.disconnect()

    def _ssl_alpn(self, root_ca: 'os.PathLike[str]',
                  certfile: 'os.PathLike[str]',
                  keyfile: 'os.PathLike[str]'):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.set_alpn_protocols(['x-amzn-mqtt-ca'])
        ssl_context.load_verify_locations(cafile=root_ca)
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        return ssl_context


def on_connect(client: mqtt.Client, userdata: Any, flags: 'dict[str, int]', rc: int):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code: {rc}")


def main():
    from pathlib import PurePath
    path = PurePath(os.path.dirname(__file__))
    thing_name = 'thing2'
    client = AwsIotClient(
        'a16tjdo0hxywt6-ats.iot.us-west-2.amazonaws.com', 443,
        root_ca=path/'AmazonRootCA1.pem',
        certfile=path/f'{thing_name}-cert.pem',
        keyfile=path/f'{thing_name}-priv.pem',
        on_connect=on_connect)
    client.publish(f'cis30d21s/{thing_name}', {"message": "hello"})
    try:
        signal.pause()
    except KeyboardInterrupt:
        client.stop()


if __name__ == '__main__':
    main()
