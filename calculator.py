import paho.mqtt.client as mqtt
from timeloop import Timeloop
from datetime import timedelta
genertor_topic = 'generator'
calculator_topic = 'calculator'
data_average = []
tl = Timeloop()


def on_message(client, userdata, msg):
    if(msg.topic == genertor_topic):
        data_average.append(int(msg.payload.decode()))

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


calculator_client = mqtt.Client()
calculator_client.on_message = on_message
calculator_client.connect("broker.hivemq.com", 1883, 60)


def average(lst):
    return sum(lst) / len(lst)


@tl.job(interval=timedelta(seconds=60))
def get_one_average():
    calculator_client.publish(
        calculator_topic, "1 Min Average: {}".format(average(data_average)))


@tl.job(interval=timedelta(seconds=300))
def get_five_average():
    calculator_client.publish(
        calculator_topic,  "5 Min Average: {}".format(average(data_average)))


@tl.job(interval=timedelta(seconds=1800))
def get_thirty_average():
    calculator_client.publish(
        calculator_topic,  "30 Min Average: {}".format(average(data_average)))


tl.start()

calculator_client.subscribe(genertor_topic, qos=1)
calculator_client.loop_forever()
