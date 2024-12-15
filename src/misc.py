import os
import json


def get_value_from_json(path: str, name: str):
    '''Returns a value from a given json file.

        Args:
            path (str): The path to JSON file to be read from.
            name (str): Name of the value to be returned.
    '''
    try:
        with open(path) as file:
            # Load the JSON content from the file
            data = json.load(file)
            # Return the value from the file
            return data[name]
    except Exception as e:
        print(e)
    return None


def write_value_to_json(path: str, name: str, value):
    '''Writes a value to a given json file, will create the file if it doesn't exist.

        Args:
            path (str): The path to JSON file to be read from.
            name (str): Name of the value to be written.
            value: Can be anything, the value to be written.
    '''
    data = {}
    try:
        # Load the JSON content from the file if found
        fileExists = os.path.isfile(path)
        if fileExists:
            with open(path) as file:
                data = json.load(file)
        # Write value
        data[name] = value
        # Update/create file
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(e)
