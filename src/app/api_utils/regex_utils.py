import re
from typing import List

dimension_regex = re.compile(r"(\d+(,\d)?(\s?x\s?)?)+")


def get_dimensions_from_description(description: str) -> List[float]:
    dimensions = dimension_regex.search(description)
    if dimensions:
        dimensions = dimensions.group() # TODO handle exceptions, more tests
        dimensions = dimensions.replace(' ', '').split('x')
        dimensions = [float(i.replace(',','.')) for i in dimensions]
    return dimensions or []
