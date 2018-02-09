#!/bin/python3
import sys
import os
import json
from typing import List, Dict, Any

def print_usage() -> None:
    print("usage")

def validate_json(json_object: Dict[str, Any]) -> List[str]:
    errors = []
    
    def key_exists(key: str) -> bool:
        if key not in json_object:
            errors.append("The property '{}' is not specified.".format(key))
            return False
        return True
    
    for prop in ["width", "height"]:
        if not key_exists(prop) and type(json_object[prop]) != int:
            errors.append("The property '{}' should be an integer but has the type '{}'.".format(
                prop, type(json_object[prop])
            ))

    if errors:
        return errors

    for prop in ["rows", "columns"]:
        if not key_exists(prop) and type(json_object[prop]) != list:
            errors.append("The property '{}' should be an array but has the type '{}'.".format(
                prop, type(json_object[prop])
            ))
            continue

        for index, array in enumerate(json_object[prop]):
            if type(array) != list:
                errors.append("The object at index {} of the property '{}' should be an array but actually is of type '{}'".format(
                    index, prop, type(array)
                ))
                continue

            for number_index, number in enumerate(array):
                if type(number) != int:
                    errors.append("The number at index {} of the array at index {} of the property '{}' should be an integer but actually has the type '{}'".format(
                        number_index, index, prop, type(number)
                    ))

    if len(json_object["rows"]) != json_object["height"]:
        errors.append("The number of rows must match the height.")
    if len(json_object["columns"]) != json_object["width"]:
        errors.append("The number of columns must match the width.")

    return errors

def process_puzzle(path: str) -> None:
    if not os.path.isfile(path):
        print("{} is not a regular file.".format(path))
        return

    try:
        f = open(path)
        json_object = json.load(f)
    except OSError as error:
        print("An error occurred while opening the file {}".format(path),
              file=sys.stderr)
        print(error.strerror, file=sys.stderr)
        return
    except json.JSONDecodeError as error:
        print("An error occurred while parsing the JSON file {}".format(path),
              file=sys.stderr)
        return
    else:
        f.close()

    errors = validate_json(json_object)
    if len(errors) > 0:
        print("The configuration file is not valid.", file=sys.stderr)
        print("Errors:", file=sys.stderr)
        print("\t", end="")
        print("\n\t".join(errors), file=sys.stderr)
        return

    # TODO run solver with validated data
    
def main() -> None:
    if len(sys.argv) < 2 or \
       any(help_command in sys.argv for help_command in ["--help", "-h", "-?"]):
        print_usage()
        return

    puzzles = len(sys.argv) - 1
    for index, path in enumerate(sys.argv[1:]):
        print("Processing puzzle {} of {}".format(index + 1, puzzles))
        process_puzzle(path)

if __name__ == "__main__":
    main()