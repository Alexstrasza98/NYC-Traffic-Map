from tomtom import get_incident_data, get_traffic_data
from utils import write_json

if __name__ == "__main__":
    print("Requesting traffic data...")
    with open("./data/coordinates_manhattan.txt", "r") as f:
        coordinates = f.readlines()

    coordinates = [coordinate.strip() for coordinate in coordinates]
    zoom = 15

    # Only fetch first 1000 samples
    traffic_data = get_traffic_data(coordinates[:1000], zoom)
    write_json(traffic_data, "./data/traffic_tomtom.json")

    print("Requesting incident data...")
    bbox = "-74.010626,40.744806,-73.960532,40.756587"
    incident_data = get_incident_data(bbox)
    write_json(incident_data, "./data/incident_tomtom.json")
