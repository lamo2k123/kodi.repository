# -*- coding: utf-8 -*-
# Name:        plugin.video.cnet
# Author:      Roman V.M.
# Created:     02.02.2014
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html

# Импортируем стандартные модули
import sys
import os
import urllib2
import xml.dom.minidom
# Импортируем xbmcswift2
from xbmcswift2 import Plugin

# Создаем объект plugin
plugin = Plugin()
# Получаем путь к плагину
addon_path = plugin.addon.getAddonInfo('path').decode('utf-8')
# Комбинируем путь к значкам
thumbpath = os.path.join(addon_path, 'resources', 'thumbnails')
# Комбинируем путь к фанарту
fanart = os.path.join(addon_path, 'fanart.jpg')
# Импортируем собственный модуль
sys.path.append(os.path.join(addon_path, 'resources', 'lib'))
from feeds import FEEDS

# Кэшируем объект, возвращаемый функцией (список), на 30 мин.
@plugin.cached(30)
def rss_parser(url):
    listing = []
    try:
        HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:18.0) Gecko/20100101 Firefox/20.0'}
        request = urllib2.Request(url, None, HEADER)
        rss = xml.dom.minidom.parse(urllib2.urlopen(request, None, 3))
    except urllib2.URLError:
        pass
    else:
        titles = rss.getElementsByTagName('title')
        links = rss.getElementsByTagName('link')
        for title, link in zip(titles[2:], links[2:]):
            title = title.toxml().replace('<title><![CDATA[', '').replace(']]></title>', '')
            link = link.toxml().replace('<link>', '').replace('</link>', '')
            listing.append((title, link))
    return listing


# Корневой путь
@plugin.route('/')
def feed_index():
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

    soup = BeautifulSoup(film.text)

    feed_list = []

    for film in soup.findAll('a', {"class" : "ui", "href" : re.compile('^details.php\?id=[0-9]+$')}):
        print film['href'], film.b.string
        feed = {'label': film.b.string,
                'path': plugin.url_for('podcast_index', feed=str(film['href']))}
        feed_list.append(feed)

    return plugin.finish(feed_list, sort_methods=['label'], view_mode=500)


# Список подкастов в разделе
@plugin.route('/feeds/<feed>')
def podcast_index(feed):
    feedNo = int(feed)
    quality = plugin.addon.getSetting('quality')
    # Получаем список подкастов в данном разделе.
    podcasts = rss_parser(url=FEEDS[feedNo][quality])
    thumb = os.path.join(thumbpath, FEEDS[feedNo]['thumb'])
    podcast_list = []
    for podcast in podcasts:
        item = {'label': podcast[0],
                'thumbnail': thumb,
                'properties': {'fanart_image': fanart},
                'path': plugin.url_for('play_podcast', url=podcast[1]),
                # Указываем, что данный объект не содержит вложенных объектов (видео для воспроизведения).
                'is_playable': True}
        podcast_list.append(item)
    # Возвращаем список подкастов без дополнительных ствойств
    return podcast_list


@plugin.route('/play/<url>')
def play_podcast(url):
    # Отдаем команду Kodi воспроизвести видео по ссылке.
    plugin.set_resolved_url(url)


if __name__ == '__main__':
    # Запускаем плагин.
    plugin.run()
