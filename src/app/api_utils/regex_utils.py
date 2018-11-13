import re
from typing import List

dimension_regex = re.compile(r"\d+(,\d)?(\s?x\s?)\d+(,\d)?((\s?x\s?)\d+(,\d)?)?")


def get_dimensions_from_description(description: str) -> List[float]:
    # TODO: add tests for hard cases
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
