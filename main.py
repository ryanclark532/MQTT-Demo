from random import randint, random
import paho.mqtt.client as mqtt
import time
topic = ''


def on_message(msg):
    print(msg.topic+" "+str(msg.payload))


def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("192.168.20.7", 1883, 60)

    while True:
        topic = str(randint(0, 100))
        print(topic)
        client.publish(topic)
        time.sleep(randint(0, 30))


main()
