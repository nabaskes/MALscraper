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
import time


def format_date(date):
    lst = date.split(" ")
    mn = lst[0]
    yr = lst[1]
    if mn == "Jan":
        mn = "01"
    elif mn == "Feb":
        mn = '02'
    elif mn == "Mar":
        mn = '03'
    elif mn == "Apr":
        mn = '04'
    elif mn == "May":
        mn = '05'
    elif mn == "Jun":
        mn = '06'
    elif mn == 'Jul':
        mn = '07'
    elif mn == 'Aug':
        mn = '08'
    elif mn == 'Sep':
        mn = '09'
    elif mn == 'Oct':
        mn = '10'
    elif mn == 'Nov':
        mn = '11'
    elif mn == 'Dec':
        mn = '12'
    else:
        raise
    return yr+"-"+mn+"-"+"01"


conn = sqlite3.connect('anime.db')


def scrape_page(resp, conn):
    soup = BeautifulSoup(resp.content, 'html.parser')
    animes = soup.find_all("tr", attrs={"class": "ranking-list"})
    # print(animes[0])

    for anime in animes:
        anime_id = str(anime.find_all("div")[1]).split("\n")[0].split("\"")[1]
        # print(anime_id)
        title = anime.find_all("a", {"id": "#"+anime_id})[1].contents[0].replace("'", "")
        # print(title)
        info_block = anime.find_all("div", attrs={"class": "information di-ib mt4"})[0].contents
        num_eps = info_block[0].replace("\n", "").replace("        ", "").replace("TV ", "").replace(" eps", "").replace("(", "").replace(")", "")
        series_run = info_block[2].replace("\n", "").replace("        ", "")
        num_votes = info_block[4].replace("\n", "").replace("        ", "").replace(",", "").replace(" members", "")
        # print(num_eps)
        # print(series_run)
        try:
            start_date = format_date(series_run.split("-")[0].strip())
        except Exception:
            start_date = None
        try:
            end_date = format_date(series_run.split("-")[1].strip())
        except Exception:
            end_date = None
        # print(num_votes)
        score = anime.find_all("span", attrs={"class": "text on"})[0].contents[0]
        # print(score)
        anime_id = anime_id.replace("area", "")
        # print(anime_id)
        c = conn.cursor()
        q = "INSERT INTO animes (ID, NAME, LENGTH, startdate, enddate, voters, score) VALUES ('{anime_id}', '{title}', '{num_eps}', '{start_date}', '{end_date}', '{num_votes}', '{score}');".format(anime_id=anime_id, title=title, num_eps=num_eps, start_date=start_date, end_date=end_date, num_votes=num_votes, score=score)
        print(q)
        c.execute(q)
    conn.commit()

for i in range(0, 14000, 50):
    print(i)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    resp = requests.get("https://myanimelist.net/topanime.php?limit="+str(i), headers = headers)
    scrape_page(resp, conn)
    time.sleep(3)
