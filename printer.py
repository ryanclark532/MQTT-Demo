import paho.mqtt.client as mqtt

one_min_average = ['0']
five_min_average = ['0']
thirty_min_average = ['0']


def on_message(client, userdata, msg):
    printer(msg.payload.decode().split(":"))


def printer(message):
    if(message[0] == "One Min Average"):
        one_min_average.append(message[1].strip())

    elif(message[0] == "Five Min Average"):
        five_min_average.append(message[1].strip())

    else:
        thirty_min_average.append(message[1].strip())
    print("One Min Average  Five Min Average  Thirty Min Average")
    print("{one: <14}   {five: <15}   {thirty:<0}".format(
        one=round(float(one_min_average[-1]), 4), five=round(float(five_min_average[-1]), 4), thirty=round(float(thirty_min_average[-1]), 4)))


printer_topic = 'calculator'

printer_client = mqtt.Client()

printer_client.on_message = on_message

printer_client.connect("127.0.0.1", 1883, 60)

printer_client.subscribe(printer_topic)

printer_client.loop_forever()
