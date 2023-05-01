import json

input_file = 'part-00000-038c425f-6e93-4a3f-95e7-47f85d896ee5-c000.json'

with open(input_file, 'r') as f:
    json_entries = f.readlines()

data = []

for entry in json_entries:
    data.append(json.loads(entry))

output_file = 'output_data.json'

with open(traffic_data, 'w') as f:
    json.dump(data, f, indent=4)

