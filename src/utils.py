import json
from statistics import median
from typing import Dict, List, Tuple, Union


def write_json(data: Union[List, Dict], json_file: str) -> None:
    with open(json_file, "w+") as outfile:
        json.dump(data, outfile)


def get_centerpoint(list_of_coords: List) -> Tuple[float, float]:
    """
    Get centerpoint of a street
    """
    if len(list_of_coords) % 2 == 1:
        centerpoint = list_of_coords[len(list_of_coords) // 2]
    else:
        centerpoint = (
            median([c[0] for c in list_of_coords]),
            median([c[1] for c in list_of_coords]),
        )
    return centerpoint
