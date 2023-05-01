from glob import glob

from utils import modify_json

if __name__ == "__main__":
    input_file = glob("./data/congestion/congestion_map/*.json")[0]
    output_file = "./data/traffic_data.json"

    modify_json(input_file, output_file)
