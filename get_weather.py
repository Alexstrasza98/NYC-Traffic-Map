import requests
import csv

with open('weather_conditions.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    code_title = header[0]
    weather_title = header[1]
    code2weather = {}
    for row in reader:
        code = row[0]
        weather = row[1]
        code2weather[code] = weather
print(code2weather)
endpoint = 'https://api.weatherapi.com/v1/current.json'
params = {
    'key': '8d74b0b642db479ebf565718231204',
    'q': 'New York',
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    updated_time = data['current']['last_updated']
    location = data['location']['name']
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_kph']
    weather_code = str(data['current']['condition']['code'])
    weather_condition = code2weather[weather_code]

    print(f"Current weather in {location}:")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind speed: {wind_speed} kph")
    print(f"Weather Condition: {weather_condition}")
else:
    print("Error: Request failed.")
