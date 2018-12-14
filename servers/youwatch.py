# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para youwatch
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core import httptools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "File Not Found" in data:
        return False, "[Youwatch] File cancellato"

    url_redirect = scrapertools.find_single_match(data, '<iframe src="([^"]+)"')
    data = httptools.downloadpage(url_redirect).data
    if "We're sorry, this video is no longer available" in data:
        return False, "[Youwatch] File cancellato"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    url_redirect = scrapertools.find_single_match(data, '<iframe src="([^"]+)"')
    data = httptools.downloadpage(url_redirect).data

    url = scrapertools.get_match(data, '{file:"([^"]+)"')
    video_url = "%s|Referer=%s" % (url, url_redirect)
    video_urls = [[scrapertools.get_filename_from_url(url)[-4:] + " [youwatch]", video_url]]

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://chouhaa.info/embed-ihc21y2tqpnt.html
    # http://youwatch.org/ihc21y2tqpnt
    # http://youwatch.to/ygzyilxutdge
    patronvideos = '(?://|\.)(?:youwatch.org|chouhaa.info|voodaith7e.com|youwatch.to)/(?:embed-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[youwatch]"
        url = "http://youwatch.org/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'youwatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve

