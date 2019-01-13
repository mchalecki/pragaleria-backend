from dateutil.relativedelta import relativedelta

PRAGALERIA_UPLOAD_URL = 'http://pragaleria.pl/wp-content/uploads/'
PRAGALERIA_AUCTIONS_URL = 'http://pragaleria.pl/aukcje-wystawy/'

DATE_FORMAT = '%Y/%m/%d %H:%M'

# Used by auctions api
PERIOD_FILTER_TYPES = {
    0: None,
    1: relativedelta(months=1),
    2: relativedelta(months=3),
    3: relativedelta(months=6),
    4: relativedelta(years=1),
}

TITLE_FILTER_TYPES = {
    0: None,
    1: "Sztuk\w Młod\w+",
    2: "Sztuk\w Aktualn\w+",
    3: "Sztuk\w Współczesn\w+",
    4: "Designu",
    5: "Malarstwa i Designu",
    6: "Wakacyjna",
}
