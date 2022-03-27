import machine
from time import sleep
import time
import network
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
