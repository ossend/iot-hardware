#!/usr/bin/python
# coding=utf-8

import json
import time
from paho.mqtt import client as mqtt

from raspi_humiture import humiture
from config import (
    broker_host, broker_port, broker_keepalive,
    publish_interval, topic, client_id, username, password
)


# 连接回调接口
def on_connect(client, userdata, flags, rc):
    print("Connecting to the MQTT server...")
    if rc == 0:
        print("Connection success")
    else:
        print("Connected with result code "+str(rc))


# publish 回调接口
def on_publish(client, userdata, mid):
    if mid == 1:
        print("A humiture has been successfully published to a topic")
    client.disconnect()


# 树莓派消息发布
def publish_message(client):
    temperature, humidity = humiture()
    client.publish(topic, payload=json.dumps({"temperature": temperature, "humidity": humidity}), qos=1)


# mqtt 连接
def connect_mqtt():
    client = mqtt.Client(client_id=client_id)
    client.username_pw_set(username, password)
    client.connect(broker_host, broker_port, broker_keepalive)
    client.on_connect = on_connect
    publish_message(client)
    client.on_publish = on_publish
    client.loop_forever()


if __name__ == '__main__':
    while True:
        connect_mqtt()
        time.sleep(publish_interval)

