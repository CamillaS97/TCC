from pickle import FALSE
from ssl import OPENSSL_VERSION
from time import sleep, time
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import json

with open("../credentials.json") as credentialsFile:
    credentialsData = json.load(credentialsFile)
    credentialsFile.close()

def getDatabaseInfo():
    try:
        conn = mysql.connector.connect(host= credentialsData['host'],
        port= credentialsData['port'],
        user= credentialsData['user'],
        password= credentialsData['password'],
        database= credentialsData['database'])

        if conn.is_connected():
            query = "SELECT * from (SELECT * from data_logs  WHERE DATE(date_time) = CURDATE() ORDER BY date_time DESC LIMIT 10)var2 ORDER BY date_time ASC;"
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            total_data = cursor.rowcount
            return data
        cursor.close()
        conn.close()
    except Error as msg:
        print(msg)

def update_plot():
    data = getDatabaseInfo()          
    temperature = []
    humidity = []
    time_date = []
    for row in data:
        temperature.append(int(row[0].replace("C", "")))
        humidity.append(int(row[1].replace("%","")))
        time_date.append(row[2].strftime("%H:%M:%S"))
    return temperature, humidity, time_date

    # plt.plot(time_date, temperature, time_date, humidity)


plt.ion()
plt.show()

while True:
    temperature, humidity, time_date = update_plot()

    plt.figure(1, figsize=(10,5))
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.yticks(temperature)
    plt.plot(time_date, temperature,color="red")
    plt.title("Temperature x Time")

    plt.figure(2, figsize=(10,5))
    plt.plot(time_date, humidity, color="orange")
    plt.xlabel("Time")
    plt.ylabel("Humidity")
    plt.yticks(humidity)
    plt.title("Humidity x Time")
    plt.draw()
    plt.pause(10)
    plt.clf()
    plt.figure(1).clear()