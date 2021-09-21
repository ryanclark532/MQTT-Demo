import paho.mqtt.client as mqtt
import time
import timerthread
from tinyPeriodicTask import TinyPeriodicTask


genertor_topic = 'generator'
calculator_topic = 'calculator'
one_min_average = []
five_min_average = []
thirty_min_average = []


def on_message(client, userdata, msg):
    if(msg.topic == genertor_topic):
        one_min_average.append(int(msg.payload.decode()))
        five_min_average.append(int(msg.payload.decode()))
        thirty_min_average.append(int(msg.payload.decode()))


calculator_client = mqtt.Client()
calculator_client.on_message = on_message
calculator_client.connect("127.0.0.1", 1883, 60)


def average(lst):
    try:
        return sum(lst) / len(lst)
    except ZeroDivisionError:
        return 0


def get_one_average():
    calculator_client.publish(
        calculator_topic, "One Min Average: {}".format(average(one_min_average)))
    one_min_average.clear()


def get_five_average():
    calculator_client.publish(
        calculator_topic,  "Five Min Average: {}".format(average(five_min_average)))
    five_min_average.clear()


def get_thirty_average():
    calculator_client.publish(
        calculator_topic,  "Thirty Min Average: {}".format(average(thirty_min_average)))
    thirty_min_average.clear()


get_one = TinyPeriodicTask(60, get_one_average)
get_five = TinyPeriodicTask(300, get_five_average)
get_thirty = TinyPeriodicTask(1800, get_thirty_average)
get_one.start()
get_five.start()
get_thirty.start()

calculator_client.subscribe(genertor_topic, qos=1)
calculator_client.loop_start()

while True:
    time.sleep(0.5)
