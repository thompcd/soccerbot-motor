import os
import json
import paho.mqtt.client as mqtt
import queue
import threading as th
import move_control

commandQueue = queue.SimpleQueue()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config["remote"]["topic"])

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if (msg.topic.endswith("move")):
        try:
            cmd = json.loads(msg.payload)
            commandQueue.put((cmd["Id"], cmd["Degrees"], cmd["Magnitude"]))
            print("added command to queue")
        except ValueError:
            print("received invalid remote command")
            
#assume dev unless prod is specified
config = None
if os.environ.get('environment') == 'prod':
    print("Loading ../config.json")
    with open("../config.json", "r") as f:
        config = json.load(f)
else:
    print("No env variable 'environment' === 'prod', loading dev config...")
    with open("../config.dev.json", "r") as f:
        config = json.load(f)
#failed to read config, must abort
if config is None:
    print("Failed to find a config.json or config.dev.json")
    raise Exception("Failed to find a config.json or config.dev.json")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config["remote"]["broker"], config["remote"]["port"], 60)

print("launching move control")
motor_thread = th.Thread(target=move_control.process_moves, args=(commandQueue, 2,))
motor_thread.start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()