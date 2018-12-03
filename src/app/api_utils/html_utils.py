from bs4 import BeautifulSoup


def clean(source):
    if source:
        clean_source = BeautifulSoup(source, "html.parser")
        source = clean_source.get_text(separator='\n').rstrip()
    return source
