from random import randint
import paho.mqtt.client as mqtt
import time
topic = 'generator'


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


generator_client = mqtt.Client()
generator_client.on_message = on_message
generator_client.on_connect = on_connect
generator_client.connect("broker.hivemq.com", 1883, 60)

while True:
    data = str(randint(0, 100))
    print(data)
    generator_client.publish(topic, data)
    time.sleep(randint(0, 30))
