import re
from typing import List

dimension_regex = re.compile(r"(\d+(,\d)?(\s?x\s?)?)+")


def get_dimensions_from_description(description: str) -> List[float]:
    # TODO: bad cases:
    # serigrafia, papier, e.a. 1/3, 67 x 49 cm (w świetle passe-partout), 85 x 66 cm (oprawa), sygn. p.d.
    # akwaforta, akwatinta, papier, 51/100, 79 x 79 cm (arkusz), 65 x 65 cm (odcisk płyty);
    # serigrafia, papier, e.a. 1/3, 67 x 49 cm (w świetle passe-partout), 85 x 66 cm (oprawa), sygn. p.d.
    # drewno, żywica epoksydowa, technika własna artysty, ed. 42-100, 7 x 11,5 x 8,5 cm, sygnowana na bocznej ścianie
    # mezzotinta, sucha igła, 10/30, 70 x 100 cm, sygn. u dołu
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
