import machine
from time import sleep
import time
import network
from umqttsimple import MQTTClient
import dht
import ujson
import urequests as requests

gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

gc.collect()

pin = machine.Pin(5, machine.Pin.OUT)
sensor = dht.DHT11(machine.Pin(14))
connected_broker = True
api_url = 'http://192.168.0.17:9898/add'
headers = {'Content-Type': 'application/json'}

#Function to connect to networks
def do_connect():
     sta_if = network.WLAN(network.STA_IF)
     if not sta_if.isconnected():
         print('connecting to network...')
         sta_if.active(True)
         sta_if.connect('NETSETUP-CamillaeFatima-2.4G', '061297100369')
         while not sta_if.isconnected():
             print("Not Connected")
     print('network connected. config:', sta_if.ifconfig())

do_connect()

# #MQTT Broker config details
# CONFIG = {
#      "MQTT_BROKER": "192.168.0.5",
#      "USER": "",
#      "PASSWORD": "",
#      "PORT": 1883,
#      "TOPIC": b"data_log",
#      # unique identifier of the chip
#      "CLIENT_ID": b"esp8266_228626"
# }

# client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
# try:
#   client.connect()
# except OSError as e:
#   print('Could not connect to Broker')
#   connected_broker = False

# #Temperature measure and upload using MQTT Broker
# if connected_broker:
#   while True:
#     try:
#       sleep(5)
#       sensor.measure()
#       temp = sensor.temperature()
#       hum = sensor.humidity()
#       print('Temperatura: ' + str(temp) + 'C')
#       print('Humidade: ' + str(hum) + '%')
#       temp = str(temp) + 'C'
#       hum = str(hum) + '%'
#       msg = ujson.dumps({'temperature': temp, 'humidity': hum})
#       print(msg)
#       client.publish(CONFIG['TOPIC'],msg)
#       sleep(55)

#     except OSError as e:
#       print('Failed to read sensor.')
# else:
#   print("Broker not connected, measuring cannot be completed")

#Temperature and upload using HTTP Post
while True:
    try:
      sensor.measure()
      temp = sensor.temperature()
      hum = sensor.humidity()
      print('Temperatura: ' + str(temp) + 'C')
      print('Humidade: ' + str(hum) + '%')
      temp = str(temp) + 'C'
      hum = str(hum) + '%'
      msg = ujson.dumps({'temperature': temp, 'humidity': hum})
      print(msg)
      try:
        response = requests.post(api_url, data= msg, headers=headers)
        print(response.json())
        response.close()
      except OSError as e:
        print(e)
      sleep(600)
    except OSError as e:
      print('Failed to read sensor.')




# pin.off()

# def onMessage(topic, msg):
#     print("Topic: %s, Message: %s" % (topic, msg))
 
#     if msg == b"on":
#         pin.on()
#     elif msg == b"off":
#         pin.off()
 
# def listen():
#     #Create an instance of MQTTClient 
#     client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
#     # Attach call back handler to be called on receiving messages
#     client.set_callback(onMessage)
#     client.connect()
#     client.publish("test", "ESP8266 is Connected")
#     client.subscribe(CONFIG['TOPIC'])
#     print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))
 
#     try:
#         while True:
#             msg = client.wait_msg()
#             #msg = (client.check_msg())
#     finally:
#         client.disconnect()  

# listen()        