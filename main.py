import os
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
# RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

# USER_AGENT = os.getenv('USER_AGENT')

WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

LATITUDE  = '35.1779'
LONGITUDE = '-111.6425'


def main():
   # get response from api
   response = get_weather()

   # print formatted weather report
   report_values = handle_response(response)

   # insert report into sql database
   insert_report(report_values)

def get_weather():
   call_url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={LATITUDE},{LONGITUDE}&days=3&aqi=no&alerts=no'

   try:
      response = requests.get(call_url)

      if response.status_code == 200:
         response = response.json()
         return response
      
      else:
         print(f"Error: {response.status_code}")

   except Exception as e:
      print(f"An error occurred: {e}")

def handle_response(response):
   current_time = response['location']['localtime']
   # formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
   formatted_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M")
   print(formatted_time)
   condition = response['current']['condition']['text']
   temp = response['current']['temp_f']
   location = response['location']['name']

   print("\n       Time: ", formatted_time)
   print("  Condition: ", condition)
   print("Temperature: ", temp)
   print("   Location: ", location)
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
