# -*- coding: utf-8 -*-

import sys
import os
import requests
import re
from xbmcswift2 import Plugin
from BeautifulSoup import BeautifulSoup

plugin = Plugin()

addon_path = plugin.addon.getAddonInfo('path').decode('utf-8')
#thumbpath = os.path.join(addon_path, 'resources', 'thumbnails')
#fanart = os.path.join(addon_path, 'fanart.jpg')
#sys.path.append(os.path.join(addon_path, 'resources', 'lib'))
#from feeds import FEEDS


#@plugin.cached(30)
# def rss_parser(url):
#     listing = []
#     try:
#         HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:18.0) Gecko/20100101 Firefox/20.0'}
#         request = urllib2.Request(url, None, HEADER)
#         rss = xml.dom.minidom.parse(urllib2.urlopen(request, None, 3))
#     except urllib2.URLError:
#         pass
#     else:
#         titles = rss.getElementsByTagName('title')
#         links = rss.getElementsByTagName('link')
#         for title, link in zip(titles[2:], links[2:]):
#             title = title.toxml().replace('<title><![CDATA[', '').replace(']]></title>', '')
#             link = link.toxml().replace('<link>', '').replace('</link>', '')
#             listing.append((title, link))
#     return listing

session = requests.session()
session.post("http://torrent.qwerty.ru/login.php", {"username": "lamo2k123", "password": "BBeriqpr2k123"})

@plugin.route('/')
def feed_index():
    return plugin.finish([{
        'label' : 'Аниме',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c12=1'))
    }, {
        'label' : 'Документальное кино и спорт',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c11=1'))
    }, {
        'label' : 'Зарубежное кино',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c6=1'))
    }, {
        'label' : 'Музыкальное видео',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c16=1'))
    }, {
        'label' : 'Мультфильмы',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c13=1'))
    }, {
        'label' : 'Сериалы',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c9=1'))
    }, {
        'label' : 'Советское и российское кино',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c8=1'))
    }, {
        'label' : 'Фильмы HD',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c24=1'))
    }, {
        'label' : 'Шоу, телепередачи, юмор',
        'path' : plugin.url_for('video_index', category=str('http://torrent.qwerty.ru/browse.php?c27=1'))
    }], sort_methods=['label'])


@plugin.route('/video/<category>')
def video_index(category):
    page = session.get(category)
    page.encoding = 'koi8-r'
    soup = BeautifulSoup(page.text)
    list = []

    for video in soup.findAll('a', {"class" : "ui", "href" : re.compile('^details.php\?id=[0-9]+$')}):
        list.append({
            'label': video.b.string,
#            'thumbnail': thumb,
#            'properties': {'fanart_image': fanart},
            'path': plugin.url_for('play_video', url=video['href']),
            'is_playable': True
        })

    return list
    #     print film['href'], film.b.string
    #     feed = {'label': film.b.string,
    #             'path': plugin.url_for('podcast_index', feed=str(film['href']))}

#     feedNo = int(feed)
#     quality = plugin.addon.getSetting('quality')
#     podcasts = rss_parser(url=FEEDS[feedNo][quality])
#     thumb = os.path.join(thumbpath, FEEDS[feedNo]['thumb'])
#     podcast_list = []
#     for podcast in podcasts:
#         item = {'label': podcast[0],
#                 'thumbnail': thumb,
#                 'properties': {'fanart_image': fanart},
#                 'path': plugin.url_for('play_podcast', url=podcast[1]),
#                 'is_playable': True}
#         podcast_list.append(item)
#     return podcast_list
#
#
@plugin.route('/play/<url>')
def play_video(url):
    plugin.set_resolved_url(url)


if __name__ == '__main__':
    plugin.run()
