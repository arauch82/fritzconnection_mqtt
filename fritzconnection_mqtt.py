#!/usr/bin/env python3

import argparse
import logging
import time
from fritzconnection import FritzConnection
import paho.mqtt.client as mqtt

fritzconnection = None
mqtt_topic = None
mqtt_string = None
fritzbox_phone = None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info(msg.topic+" "+str(msg.payload))
    if msg.payload.decode('utf-8') == mqtt_string:
        logging.info("Code received, trigger Fritzbox call!")
        arg = {'NewX_AVM-DE_PhoneNumber': fritzbox_phone}
        fritz_connection.call_action('X_VoIP1', 'X_AVM-DE_DialNumber', arguments=arg)
        time.sleep(5)
        fritz_connection.call_action('X_VoIP1', 'X_AVM-DE_DialHangup')

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Triggers a phone call on a Fritzbox when a certain message is received on an mqtt topic')
parser.add_argument('--mqtt_server', dest='mqtt_server', type=str, default='192.168.178.97',
                    help="MQTT server")
parser.add_argument('--mqtt_topic', dest='mqtt_topic', type=str, default='/rf/receive',
                    help="MQTT input topic")
parser.add_argument('--mqtt_string', dest='mqtt_string', type=str, default='15555555',
                    help="MQTT input string to trigger phonecall")
parser.add_argument('--fritzbox_ip', dest='fritzbox_ip', type=str, default="192.168.178.1",
                    help="IP address of Fritzbox")
parser.add_argument('--fritzbox_password', dest='fritzbox_password', type=str, required=True,
                    help="Password of Fritzbox")
parser.add_argument('--fritzbox_phone', dest='fritzbox_phone', type=str, default='**611',
                    help="Phone number to call")
args = parser.parse_args()

mqtt_topic = args.mqtt_topic
mqtt_string = args.mqtt_string
fritzbox_phone = args.fritzbox_phone

fritz_connection = FritzConnection(address=args.fritzbox_ip, password=args.fritzbox_password)
logging.info("Established connection to Fritzbox")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.mqtt_server, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()