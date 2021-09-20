import paho.mqtt.client as mqtt
from timeloop import Timeloop
from datetime import timedelta
genertor_topic = 'generator'
calculator_topic = 'calculator'
one_min_average = []
five_min_average = []
thirty_min_average = []
tl = Timeloop()


def on_message(client, userdata, msg):
    if(msg.topic == genertor_topic):
        one_min_average.append(int(msg.payload.decode()))
        five_min_average.append(int(msg.payload.decode()))
        thirty_min_average.append(int(msg.payload.decode()))


calculator_client = mqtt.Client()
calculator_client.on_message = on_message
calculator_client.connect("127.0.0.1", 1883, 60)


def average(lst):
    return sum(lst) / len(lst)


@tl.job(interval=timedelta(seconds=60))
def get_one_average():
    calculator_client.publish(
        calculator_topic, "One Min Average: {}".format(average(one_min_average)))
    one_min_average.clear()


@tl.job(interval=timedelta(seconds=300))
def get_five_average():
    calculator_client.publish(
        calculator_topic,  "Five Min Average: {}".format(average(five_min_average)))
    five_min_average.clear()


@tl.job(interval=timedelta(seconds=1800))
def get_thirty_average():
    calculator_client.publish(
        calculator_topic,  "Thirty Min Average: {}".format(average(thirty_min_average)))
    thirty_min_average.clear()


tl.start()

calculator_client.subscribe(genertor_topic, qos=1)
calculator_client.loop_forever()
