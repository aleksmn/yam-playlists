import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

URL = input(
    "Введите ссылку на плейлист: ") or "https://music.yandex.com/users/yamusic-top/playlists/1035"
CSV_FILE_NAME = input("Введите название файла: ") or "Electronica-best"

# Количество прокруток (увеличить, если не доходит до конца плейлиста):
SCROLL_COUNT = 5

track_list = []

# Selenium

driver = webdriver.Chrome()

driver.get(URL)

driver.implicitly_wait(2)

# Закрыть рекламное окно
try:
    driver.find_element("class name", "d-icon_cross-big").click()
except:
    pass


def scroll_page(n=5):
    element = driver.find_element("tag name", 'body')
    for i in range(n):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)


for n in range(SCROLL_COUNT):
    time.sleep(0.1)

    tracks = driver.find_elements("class name", "d-track")

    for t in tracks:
        title = t.find_element("class name", "d-track__title").text
        artist = t.find_element("class name", "d-track__artists").text
        link_element = t.find_element("class name", "d-track__title")
        link = link_element.get_attribute("href")

        track_item = {
            'title': title,
            'artist': artist,
            'link': link
        }
        track_list.append(track_item)

    scroll_page()


df = pd.DataFrame(track_list)

df.drop_duplicates(inplace=True)

print(df)


df.to_csv(CSV_FILE_NAME + ".csv", index=False, sep=';')
