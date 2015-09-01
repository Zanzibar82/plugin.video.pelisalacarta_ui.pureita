# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinestreaming01.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinestreaming01"
__category__ = "F"
__type__ = "generic"
__title__ = "Cinestreaming01"
__language__ = "IT"

DEBUG = config.get_setting("debug")

sito="http://www.cinestreaming01.com"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.cinestreaming01 mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Ultimi Film Inseriti[/COLOR]", action="peliculas", url=sito, thumbnail="http://dc584.4shared.com/img/XImgcB94/s7/13feaf0b538/saquinho_de_pipoca_01"))
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Film Per Categoria[/COLOR]", action="categorias", url=sito, thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"))
    itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Cerca...[/COLOR]", action="search", thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"))

    
    return itemlist

def categorias(item):
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.get_match(data,'<ul class="main-menu clearfix">(.*?)</ul>')
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR azure]"+scrapedtitle+"[/COLOR]" , url=sito+scrapedurl , thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png", folder=True) )

    return itemlist

def search(item,texto):
    logger.info("[cinestreaming01.py] "+item.url+" search "+texto)
    item.url = "http://cinestreaming01.com/?s="+texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.cinestreaming01 peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    #patron = '<div class="boxim">\s*'
    patron = '<div class="box " id="post-.*?">.*?<a href="(.*?)"><img class="boximg" src="http://cinestreaming01.com/wp-content/themes/Boxoffice/timthumb.php?src=(.*?)&amp;h=270&amp;w=180&amp;zc=1" alt=""/></a>\s*'
    patron += '<h2><a href=".*?" rel="bookmark" title=".*?">(.*?)</a></h2>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        #scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming e download ita ",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title="[COLOR azure]"+scrapedtitle+"[/COLOR]" , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<span class="pnext"><a href="(.*?)">Avanti</a></span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR orange]Successivo>>[/COLOR]" , url=scrapedurl , thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png", folder=True) )

    return itemlist
