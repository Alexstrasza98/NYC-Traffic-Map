from apis import get_weather_data
from utils import write_json

if __name__ == "__main__":
    # Requesting weather data
    print("Requesting weather data...")
    with open("./data/coordinates_manhattan.txt", "r") as f:
        coordinates = f.readlines()

    coordinates = [coordinate.strip() for coordinate in coordinates]
    weather_data = get_weather_data(coordinates)
    write_json(weather_data, "./data/weather.json")
