# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para 1fichier
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------

import re
import urllib

from core import config
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("streamondemand.servers.onefichier get_video_url(page_url='%s')" % page_url)

    video_urls = []

    if config.get_setting("onefichierpremium") == "true":
        user = config.get_setting("onefichieruser")
        password = config.get_setting("onefichierpassword")

        url = "https://1fichier.com/login.pl"
        logger.info("streamondemand.servers.onefichier url=" + url)
        post_parameters = {"mail": user, "pass": password, "lt": "on", "purge": "on", "valider": "Send"}
        post = urllib.urlencode(post_parameters)
        logger.info("streamondemand.servers.onefichier post=" + post)

        scrapertools.cache_page(url, post=post)
        # logger.info("streamondemand.servers.onefichier data="+data)

        cookies = config.get_cookie_data()
        logger.info("streamondemand.servers.onefichier cookies=" + cookies)

        # 1fichier.com   TRUE    /   FALSE   1443553315  SID imC3q8MQ7cARw5tkXeWvKyrH493rR=1yvrjhxDAA0T0iEmqRfNF9GXwjrwPHssAQ
        sid_cookie_value = scrapertools.find_single_match(cookies, "1fichier.com.*?SID\s+([A-Za-z0-9\+\=]+)")
        logger.info("streamondemand.servers.onefichier sid_cookie_value=" + sid_cookie_value)

        # .1fichier.com  TRUE    /   FALSE   1443553315  SID imC3q8MQ7cARw5tkXeWvKyrH493rR=1yvrjhxDAA0T0iEmqRfNF9GXwjrwPHssAQ
        cookie = urllib.urlencode({"SID": sid_cookie_value})

        # Averigua el nombre del fichero real
        filename = scrapertools.get_header_from_response(page_url, header_to_get="Content-Disposition")
        logger.info("streamondemand.servers.onefichier filename=" + filename)

        # Construye la URL final para Kodi
        location = page_url + "|Cookie=" + cookie
        logger.info("streamondemand.servers.onefichier location=" + location)

        video_urls.append([filename[-4:] + " (Premium) [1fichier]", location])

    for video_url in video_urls:
        logger.info("streamondemand.servers.onefichier %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://kzu0y3.1fichier.com/
    patronvideos = '([a-z0-9]+\.1fichier.com)'
    logger.info("streamondemand.servers.onefichier find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[onefichier]"
        url = "https://1fichier.com/?" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'onefichier'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # https://1fichier.com/?s6gdceia9y
    patronvideos = '1fichier.com/\?([a-z0-9]+)'
    logger.info("streamondemand.servers.onefichier find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[onefichier]"
        url = "https://1fichier.com/?" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'onefichier'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
