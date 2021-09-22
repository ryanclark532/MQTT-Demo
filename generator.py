from random import randint
import paho.mqtt.client as mqtt
import time
topic = 'generator'
generator_client = mqtt.Client()
generator_client.connect("localhost", 1883)

while True:
    data = str(randint(0, 100))
    print(data)
    generator_client.publish(topic, data)
    time.sleep(randint(0, 30))
