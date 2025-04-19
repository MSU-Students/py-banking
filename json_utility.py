import json
import os

# Function to write data to a JSON file
def write_json(filename, data):
    # Define the path to the JSON file in the 'data' folder
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to read data from a JSON file
def read_json(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return None  # or return empty data structure if file doesn't exist
