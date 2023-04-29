from tomtom import get_incident_data, get_traffic_data
from utils import write_json

if __name__ == "__main__":
    # print("Requesting traffic data...")
    # with open("./data/coordinates_manhattan.txt", "r") as f:
    #     coordinates = f.readlines()

    # coordinates = [coordinate.strip() for coordinate in coordinates]
    # zoom = 15

    # # Only fetch first 1000 samples
    # traffic_data = get_traffic_data(coordinates[:1000], zoom)
    # write_json(traffic_data, "./data/traffic_tomtom.json")

    print("Requesting incident data...")
    incident_data = []
    bboxs = [
        "-74.017191,40.701654,-73.970910,40.750482",
        "-74.003519,40.756170,-73.944322,40.784978",
        "40.789491 -73.980009,-73.930612,40.814190",
    ]
    for bbox in bboxs:
        incident_data.append(get_incident_data(bbox))
    write_json(incident_data, "./data/incident_tomtom.json")
