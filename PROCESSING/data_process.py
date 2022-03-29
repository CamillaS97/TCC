from ssl import OPENSSL_VERSION
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime, timedelta
import re
import json


#initializing all temperature and humidity variables as 0 for easier comparison aftewards
higher_temp = higher_hum = lower_temp = lower_hum = temp_total = temp_anterior = alerta = alerta_high = 0
file_name = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

def log_messages(data_list):
    logging.basicConfig(filename= file_name + '.log', filemode='w', level=logging.DEBUG, format='%(levelname)s: %(message)s')
    i=0
    for data in data_list:
        if(i < 5):
            logging.info(data_list[i])
        else:
            if(re.search(r'\b0\b', data_list[i])):
                logging.info(data_list[i])
            else:
                logging.warning(data_list[i])
        i = i+1

with open("../credentials.json") as credentialsFile:
    credentialsData = json.load(credentialsFile)
    credentialsFile.close()

try:
    conn = mysql.connector.connect(host= credentialsData['host'],
      port= credentialsData['port'],
      user= credentialsData['user'],
      password= credentialsData['password'],
      database= credentialsData['database'])

    if conn.is_connected():
      query = "select * from data_logs  WHERE DATE(date_time) = CURDATE() - 1;"
      cursor = conn.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      total_data = cursor.rowcount

except Error as msg:
    print(msg)

for row in data:
    temperature = int(row[0].replace("C", ""))
    humidity = int(row[1].replace("%",""))
    temp_total = temperature + temp_total

    if(temperature > higher_temp):
        higher_temp = temperature
        msg_temp = "Maior temperatura: " + str(higher_temp) + "C. Horario: " + str(row[2])

    if(temperature < lower_temp or lower_temp == 0):
        lower_temp = temperature
        msg_low_temp = "Menor tempertaura: " + str(lower_temp) + "C. Horario " + str(row[2])

    if(humidity > higher_hum):
       higher_hum = humidity
       msg_hum = "Maior humidade: " + str(higher_hum) + "%. Horario: " + str(row[2])
       
    if(humidity < lower_hum or lower_hum == 0):
        lower_hum = humidity
        msg_low_hum = "Menor humidade: " + str(lower_hum) + "%. Horario: " + str(row[2])

    if (temperature >= 30):
        alerta_high = alerta_high+1

    if (temp_anterior != 0):
        if(temp_anterior - temperature >= 4 or temp_anterior - temperature <= -4 ):
            alerta = alerta + 1            
    else:
        temp_anterior = temperature
    
    temp_anterior = temperature

average_temp = temp_total/total_data
msg_average = "Temperatura media: " + str(average_temp)
msg_alerta = str(alerta) + " variacoes bruscas ocorreram"
msg_superaq = "A temperatura ultrapassou o valor maximo em " + str(alerta_high) + " vezes"

log_messages([msg_temp, msg_low_temp, msg_hum, msg_low_hum, msg_average, msg_alerta, msg_superaq])


cursor.close()
conn.close()