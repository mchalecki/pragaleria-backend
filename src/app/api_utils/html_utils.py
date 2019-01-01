import re

from bs4 import BeautifulSoup

URLS_TEMPLATES = {
    'virtual_tour': 'wnetrza3d.pl/realizacje/pragaleria/',
    'bidding': 'onebid.pl/pl/aukcje/-/'
}


def clean(source, urls=False):
    if not source:
        return source if not urls else (source, {k: None for k in URLS_TEMPLATES})
    soup = BeautifulSoup(source, "html.parser")
    text = soup.get_text(separator='\n')
    text = '\n'.join(text.splitlines())
    text = re.sub(r'\n+', '\n', text)
    text = text.replace('\n \n', '\n')
    text = text.strip()
    text = text.replace('&quot;', '""')
    if not urls:
        return text
    else:
        links = soup.find_all('a')
        templates = URLS_TEMPLATES.copy()
        existing_urls = {k: None for k in URLS_TEMPLATES}
        for link in links:
            link = link.get('href')
            for name, url_template in dict(templates).items():
                if url_template in link:
                    existing_urls[name] = link
                    templates.pop(name)
        return text, existing_urls
