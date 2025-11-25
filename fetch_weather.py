#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = os.getenv("MYSQL_HOST")

CITY = 'Oulu'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=fi'

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)

cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (id INT
AUTO_INCREMENT PRIMARY KEY, city VARCHAR(50), temperature FLOAT, description
VARCHAR(100), timestamp DATETIME)''')
response = requests.get(URL)
data = response.json()
temp = data['main']['temp']
desc = data['weather'][0]['description']
wind_speed = data['wind']['speed']
helsinki_tz = pytz.timezone('Europe/Helsinki')
timestamp = datetime.now(helsinki_tz)
cursor.execute('INSERT INTO weather_data (city, temperature, description, wind_speed, timestamp) VALUES (%s, %s, %s, %s, %s)', (CITY, temp, desc, wind_speed, timestamp))
conn.commit()
cursor.close()
conn.close()
print(f'Data tallennettu: {CITY} {temp}°C {desc}')
