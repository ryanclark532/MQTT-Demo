import paho.mqtt.client as mqtt
import time
import schedule

genertor_topic = 'generator'
calculator_topic = 'calculator'
one_min_average = []
five_min_average = []
thirty_min_average = []


def on_message(client, userdata, msg):
    print('Message Recived')
    if(msg.topic == genertor_topic):
        one_min_average.append(int(msg.payload.decode()))
        five_min_average.append(int(msg.payload.decode()))
        thirty_min_average.append(int(msg.payload.decode()))


def on_publish(client, userdata, mid):
    print("{} {} {}".format(client, userdata, mid))


calculator_client = mqtt.Client()
calculator_client.on_message = on_message
calculator_client.on_publish = on_publish
calculator_client.connect("localhost", 1883)


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


calculator_client.subscribe(genertor_topic, qos=1)
calculator_client.loop_start()


schedule.every(1).minutes.do(get_one_average)
schedule.every(5).minutes.do(get_five_average)
schedule.every(30).minutes.do(get_thirty_average)
while True:
    schedule.run_pending()
    time.sleep(0.01)
