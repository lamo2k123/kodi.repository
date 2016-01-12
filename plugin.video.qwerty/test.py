import sys
import os

import cookielib
import urllib
import urllib2

import requests
import re
from BeautifulSoup import BeautifulSoup

data = {"username": "lamo2k123", "password": "BBeriqpr2k123"}

session = requests.session()

r = session.post("http://torrent.qwerty.ru/login.php", data)
r.encoding = 'koi8-r'
print r.text


film = session.get("http://torrent.qwerty.ru/browse.php?c6=1")
film.encoding = 'koi8-r'

prog = re.compile(r'<a class="ui" href="details.php\?id=[0-9]+"><b>([\w\s/\[\],]+)</b></a>', re.M)
soup = BeautifulSoup(film.text)

for film in soup.findAll('a', {"class" : "ui", "href" : re.compile('^details.php\?id=[0-9]+$')}):
    print film['href'], film.b.string