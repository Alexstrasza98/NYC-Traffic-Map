from typing import List, Dict, Union
import json


def write_json(data: Union[List, Dict], json_file: str) -> None:
    with open(json_file, "w") as outfile:
        json.dump(data, outfile)
