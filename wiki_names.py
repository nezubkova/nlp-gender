import json
import requests

from bs4 import BeautifulSoup

male_page = 'https://ru.wikipedia.org/wiki/Категория:Русские_мужские_имена'
female_page = 'https://ru.wikipedia.org/wiki/Категория:Русские_женские_имена'

headers = {'User-Agent': user_agent}


def extract_names(page: str):
    """
    This function lets us extract names from wiki page
    """
    response = requests.get(page, headers=headers, verify=False)
    bs = BeautifulSoup(response.text)
    return list(
        map(
            lambda x: x.text,
            bs.find_all(
                'li', attrs={'class': None, 'id': None, 'title': None}
            )
        )
    )[:-2]


def split_name(name_src: str):
    """
    This functions drops (имя) in the end of the wiki link
    """
    return name_src.split()[0]


male_names = list(map(split_name, extract_names(male_page)[1:]))
female_names = list(map(split_name, extract_names(female_page)))
