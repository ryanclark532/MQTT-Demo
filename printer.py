import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


calculator_topic = 'calculator'

calculator_client = mqtt.Client()

calculator_client.on_message = on_message

calculator_client.connect("broker.hivemq.com", 1883, 60)

calculator_client.subscribe(calculator_topic)

calculator_client.loop_forever()
