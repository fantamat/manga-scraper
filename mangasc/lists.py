import re
import requests
import logging


def get_boruto_manga_list():
    response = requests.get("https://w15.read-borutomanga.com/")
    if response.status_code != 200:
        logging.error("Failed to retrieve manga list. Status code: %d", response.status_code)
        return []
    
    pattern = re.compile(r'<li><a href="https://w15.read-borutomanga.com/manga/[^"]*">[^<]*</a></li>')

    find_patterns = re.findall(pattern, response.text)

    manga_list = {}
    for item in find_patterns:
        url_start = item.find('href="') + len('href="')
        url_end = item.find('"', url_start)
        manga_url = item[url_start:url_end]

        name_start = item.find('>', url_end) + len('>')
        name_end = item.find('</a>', name_start)
        manga_name = item[name_start:name_end]

        manga_list[manga_name] = manga_url
    return manga_list