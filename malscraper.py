##########################################################
#
#
# Scraper for myanimelist.net
#
#
#
###########################################################
from bs4 import BeautifulSoup
import requests
import sqlite3


conn = sqlite3.connect('anime.db')



resp = requests.get("https://myanimelist.net/topanime.php?")
soup = BeautifulSoup(resp.content, 'html.parser')
animes = soup.find_all("tr", attrs={"class": "ranking-list"})
# print(animes[0])

for anime in animes:
    anime_id = str(anime.find_all("div")[1]).split("\n")[0].split("\"")[1]
    print(anime_id)
    title = anime.find_all("a", {"id": "#"+anime_id})[1].contents[0]
    print(title)
    info_block = anime.find_all("div", attrs={"class": "information di-ib mt4"})[0].contents
    series_format = info_block[0].replace("\n", "").replace("        ", "")
    series_run = info_block[2].replace("\n", "").replace("        ", "")
    print(series_format)
    print(series_run)
    score = anime.find_all("span", attrs={"class": "text on"})[0].contents[0]
    print(score)
