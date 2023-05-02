import json
from statistics import median
from typing import Dict, List, Tuple, Union


def write_json(data: Union[List, Dict], json_file: str) -> None:
    with open(json_file, "w+") as outfile:
        json.dump(data, outfile)


def read_json(json_file: str) -> Union[List, Dict]:
    with open(json_file, "r") as infile:
        data = json.load(infile)
    return data


def get_centerpoint(list_of_coords: List) -> Tuple[float, float]:
    """
    Get centerpoint of a street
    """
    if len(list_of_coords) % 2 == 1:
        centerpoint = list_of_coords[len(list_of_coords) // 2]
    else:
        centerpoint = [
            median([c[0] for c in list_of_coords]),
            median([c[1] for c in list_of_coords]),
        ]
    return centerpoint


def modify_jsons(input_files, output_file):
    """
    Modify json single line file into multiple line file
    """
    data = []

    for input_file in input_files:
        with open(input_file, "r") as f:
            json_entries = f.readlines()

        for entry in json_entries:
            data.append(json.loads(entry))

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
