import pandas as pd
import time

from bs4 import BeautifulSoup
from selenium import webdriver as wb

br = wb.Chrome(r'/Users/m.e.zubkova/Downloads/chromedriver-3')
iteration1 = 1
iteration2 = 1
urls = []

br.get('https://profi.ru/it_freelance/designer/?seamless=1&tabName=PROFILES&sort=reviews')

while True:
    field = br.find_elements_by_xpath("//*[contains(text(), 'Показать ещё')]")[0]
    field.click()
    time.sleep(3)
    if iteration1 % 10 == 0:
        print(iteration1)
        time.sleep(60)

source = BeautifulSoup(br.page_source).find_all('a', attrs={'class': 'ui_1hi7c'})

for i in range(len(source)):
    try:
        if source[i].get('href').startswith(
                '/it_freelance/designer/?seamless=1'
        ):
            urls.append(source[i].get('href'))
    except:
        pass

data = pd.DataFrame(columns=['marks', 'texts', 'author_names', 'profile', 'freelancer_name'])

for url in urls:
    try:
        br.get('https://profi.ru' + url)  # переходим на рандомного пользователя
        bs = BeautifulSoup(br.page_source)  # открываем его страницу
        reviews = bs.find_all('div', attrs={'data-shmid': 'ReviewItem'})  # список отзывов
        marks = []
        texts = []
        author_names = []
        for i in range(len(reviews)):
            try:
                marks.append(
                    reviews[i].find(
                        'div', attrs={'class': 'ui_1g_zG ui_3kLkk'}
                    ).find(
                        'p', attrs={'class': 'ui_2MYaG ui_2SXfw ui_RF7aD ui_1hoX9'}
                    ).text
                )
            except:
                marks.append(len(reviews[i].find_all('svg', attrs={"class": "ui_1BBoM ui_366n3"})))
            try:
                texts.append(
                    reviews[i].find('div', attrs={'class': 'ui-text _MUmGtQr _3xKhc83 _2iyzK60 _1A6uUTD'}).text
                )
            except:
                texts.append('Нет отзыва')

            author_names.append(
                reviews[i].find(
                    'div', attrs={'class': 'ui-text _2cila-e _3xKhc83 _2iyzK60'}
                ).text
            )
        profile_df = pd.DataFrame([marks, texts, author_names]).T.rename(
            columns={0: 'marks', 1: 'texts', 2: 'author_names'})
        profile_df['profile'] = br.current_url
        profile_df['freelancer_name'] = bs.find_all('h1', attrs={'data-shmid': 'profilePrepName'})[0].text
        data = pd.concat((data, profile_df))
        iteration2 += 1
    except:
        pass

    if iteration2 % 10 == 0:
        print(data.shape)
        time.sleep(40)
