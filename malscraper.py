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
