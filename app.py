import time
import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# URL = "https://music.yandex.ru/users/al-mn/playlists/1044"
# CSV_FILE_NAME = "indy"

URL = input("Введите ссылку на плейлист: ") or "https://music.yandex.ru/users/al-mn/playlists/1044"
CSV_FILE_NAME = input("Введите название файла: ") or "indy"
# Количество прокруток (увеличить, если не доходит до конца плейлиста):
SCROLL_COUNT = 5

track_list = []

# Using Selenium

driver = webdriver.Chrome()


driver.get(URL)

def scroll_page(n=5):
  element = driver.find_element("tag name", 'body')
  for i in range(n):
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)


for n in range(SCROLL_COUNT):
  time.sleep(1)

  tracks = driver.find_elements("class name", "d-track")


  for t in tracks:
    title = t.find_element("class name", "d-track__title").text
    artist = t.find_element("class name","d-track__artists").text
    link_element = t.find_element("class name", "d-track__title")
    link = link_element.get_attribute("href")
    # link = url_base+link

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


df.to_csv(CSV_FILE_NAME +".csv", index=False, sep=';')

