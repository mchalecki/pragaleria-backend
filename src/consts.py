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
    1: "Aukcja Sztuka Młoda",
    2: "Aukcja Sztuka Aktualna",
    3: "Aukcja Sztuki Współczesnej",
    4: "Aukcja Designu",
    5: "Aukcja Malarstwa i Designu",
    6: "Wakacyjna",
}
