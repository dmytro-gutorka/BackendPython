from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.getenv("API_KEY")
city_name = input(str('Enter your city name: \n'))
URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'


response = requests.get(URL).json()

print(f"Current weather in {city_name} - {response['weather'][0]['description']} \n"
      f"Max temperature: {response['main']['temp_max']} °F \n"
      f"Min temperature: {response['main']['temp_min']} °F \n")

