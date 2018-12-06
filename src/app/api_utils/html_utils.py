import re

from bs4 import BeautifulSoup


def clean(source):
    if source:
        clean_source = BeautifulSoup(source, "html.parser")
        text = clean_source.get_text(separator='\n')
        text = '\n'.join(text.splitlines())
        text = re.sub(r'\n+', '\n', text)
        text = text.replace('\n \n', '\n')
        text = text.strip()
        text = text.replace('&quot;', '""')
        source = text
    return source
