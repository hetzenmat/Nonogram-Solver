from typing import List, Dict, Tuple, Any, Type

class Constraints:

    def __init__(self, width, height, rows, columns):
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns

    @staticmethod
    def validate_json(json_object: Dict[str, Any]) -> Tuple[List[str], "Constraints"]:
        """
        Checks if the given JSON object is valid.
        It returns a tuple of a list of errors and an instance of Constraints.
        If errors are present the instance is None and if no errors were found the
        list of errors is empty. 
        """
        errors = []
    
        def key_exists(key: str) -> bool:
            if key not in json_object:
                errors.append("The property '{}' is not specified.".format(key))
                return False
            return True
        
        for prop in ["width", "height"]:
            if key_exists(prop) and type(json_object[prop]) != int:
                errors.append("The property '{}' should be an integer but has the type '{}'.".format(
                    prop, type(json_object[prop])
                ))

        if errors:
            return errors, None

        for prop in ["rows", "columns"]:
            if not key_exists(prop):
                continue

            if type(json_object[prop]) != list:
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
                        continue
                    
                    if number <= 0:
                        errors.append("The number at index {} of the array at index {} of the property '{}' is smaller or equal than zero but should actually be a positive integer.".format(
                            number_index, index, prop
                        ))

        if errors:
            return errors, None

        if len(json_object["rows"]) != json_object["height"]:
            errors.append("The number of rows must match the height.")
        if len(json_object["columns"]) != json_object["width"]:
            errors.append("The number of columns must match the width.")

        if errors:
            return errors, None

        # check if the sum of blocks does exceeds the size of the puzzle
        for index, row in enumerate(json_object["rows"]):
            if sum(row) > json_object["width"]:
                errors.append("The sum of the blocks at the row with index {} exceeds the width.".format(
                    index
                ))

        for index, column in enumerate(json_object["columns"]):
            if sum(column) > json_object["height"]:
                errors.append("The sum of the blocks at the column with index {} exceeds the height.".format(
                    index
                ))

        if errors:
            return errors, None

        return [], Constraints(json_object['width'],
                               json_object['height'],
                               json_object['rows'],
                               json_object['columns'])
