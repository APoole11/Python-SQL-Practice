import os
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

def main():
   # get response from api
   response = get_weather()

   # print formatted weather report
   report_values = print_report(response)

   # insert report into sql database
   insert_report(report_values)

def get_weather():
   url = "https://open-weather13.p.rapidapi.com/city/flagstaff"

   headers = {
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "X-RapidAPI-Host": RAPIDAPI_HOST
   }

   response = requests.get(url, headers=headers)
   return response.json()

def print_report(response):
   current_time = datetime.now()
   formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
   condition = response['weather'][0]['main']
   temp = response['main']['temp']
   location = response['name']

   print("\nTime: ", formatted_time)
   print("Condition: ", condition)
   print("Temperature: ", temp)
   print("Location: ", location)
   print("\n")

   return [formatted_time, condition, temp, location]
   
def insert_report(report_values):

   conn = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASSWORD,
      database=DB_DATABASE
   )

   cursor = conn.cursor()

   try:
      insert_query = "INSERT INTO weather_log (curr_datetime, curr_condition, curr_temperature, curr_location) VALUES (%s, %s, %s, %s)"
      entry_data = (report_values[0], report_values[1], report_values[2], report_values[3])

      cursor.execute(insert_query, entry_data)

      conn.commit()
      print("Successfully inserted into 'flagstaff_weather' database\n")

   except Exception as e:
      conn.rollback()
      print(f"Error: {e}")

   finally:
      cursor.close()
      conn.close()

if __name__ == '__main__':
   main()
