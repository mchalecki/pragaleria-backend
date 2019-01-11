import re
from typing import List

dimension_regex = re.compile(r"\d+(,\d+)?(\s?x\s?)\d+(,\d+)?((\s?x\s?)\d+(,\d+)?)?")


def get_dimensions_from_description(description):
    dimensions = dimension_regex.search(description)
    if dimensions:
        dimensions = dimensions.group()  # TODO handle exceptions, more tests
        dimensions = dimensions.replace(' ', '').split('x')
        try:
            dimensions = [float(i.replace(',', '.')) for i in dimensions if i]
        except ValueError:
            print(f"Couldn't parse {dimensions} from {description}")
            dimensions = []
    return dimensions or []


def string_to_bool(string):
    false_strings = ['0', 'false', 'False']
    true_strings = ['1', 'true', 'True']
    if string in false_strings:
        return False
    elif string in true_strings:
        return True
    return None
