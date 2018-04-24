# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmsenzalimiti_info
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------

import base64
import re
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmsenzalimiti_info"
host = "https://www.filmsenzalimiti.info"
headers = [['Referer', host]]


def mainlist(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] mainlist")

    itemlist = [
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Novita'[/COLOR]",
             action="peliculas_movie",
             url=host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_new.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Aggiornati[/COLOR]",
             action="peliculas",
             url="%s/watch-genre/featured/" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_new_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - HD[/COLOR]",
             action="peliculas",
             url="%s/watch-genre/altadefinizione" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/blueray_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - 3D[/COLOR]",
             action="peliculas",
             url="%s/watch-genre/3d" % host,
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_3D_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Film[COLOR orange] - Categorie[/COLOR]",
             action="genere",
             url=host,
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV[COLOR orange] - Novita'[/COLOR]",
             action="peliculas_tv",
             url="%s/watch-genre/serie-tv" % host,
             extra="serie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_serie_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV[COLOR orange] - TV Show[/COLOR]",
             action="peliculas_tv",
             url="%s/watch-genre/programmi-tv" % host,
             extra="serie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/new_tvshows_P.png"),
        Item(channel=__channel__,
             title="[COLOR azure]Serie TV[COLOR orange] - Miniserie[/COLOR]",
             action="peliculas_tv",
             url="%s/watch-genre/miniserie" % host,
             extra="serie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/tv_series_P.png"),
        Item(channel=__channel__,
             title="[COLOR orange]Cerca...[/COLOR]",
             action="search",
             extra="movie",
             thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist

# ==============================================================================================================================================================================

def search(item, texto):
    logger.info("[streamondemand-pureita filmsenzalimiti_info]  " + item.url + " search " + texto)

    item.url = host + "/?s=" + texto

    try:
        return peliculas_movie(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

# ==================================================================================================================================================		

def genere(item):
    logger.info("[streamondemand-pureita guarda_serie] genere")
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, "<a href='[^']+'>Anime</a></option>(.*?)Serie TV</a></option>")

    # Extrae las entradas (carpetas)
    patron = "<a href='([^']+)'>([^<]+)</a></option>"
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist

# ==================================================================================================================================================

def peliculas(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data	
	
    patron = 'a href="([^"]+)"><img width[^>]+ src="([^"]+)"\s*'
    patron += 'class[^>]+ alt=""[^>]+></a>[^>]+>[^>]+><p>([^<]+)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace(" streaming", "").replace(":", "")
        scrapedtitle = scrapedtitle.replace("-)", ")").replace("’", "'")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos_movie",
                 contentType="movie",
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def peliculas_tv(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] peliculas")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data	
	
    patron = 'a href="([^"]+)"><img width[^>]+ src="([^"]+)"\s*'
    patron += 'class[^>]+ alt=""[^>]+></a>[^>]+>[^>]+><p>([^<]+)</p>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.replace(" streaming", "").replace(":", "")
        scrapedtitle = scrapedtitle.replace("-)", ")").replace("’", "'")
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="serie",
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 folder=True), tipo='tv'))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def peliculas_movie(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] peliculas_movie")

    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data	

    patron = '<div class=".*?genre-(.*?)"\s*id[^>]+>\s*[^>]+>.*?'
    patron += '<a href="([^"]+)" title="([^<]+)" rel="bookmark">\s*'
    patron += '<img width[^>]+src="([^"]+)" class[^>]+>.*?<p>(.*?)</p>'


    matches = re.compile(patron, re.DOTALL).findall(data)

    for genre, scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot  in matches:
        if " sub-ITA" in scrapedtitle or " sub-ITA]" in scrapedtitle:
          lang = " [[COLOR yellow]" + "Sub ITA" + "[/COLOR]]"
        if "anime" in genre:
          continue
        scrapedtitle = scrapedtitle.replace("Permalink to ", "").replace(" streaming", "")
        scrapedtitle = scrapedtitle.replace(" sub-ITA", "").replace(" sub-ITA]", "")
        scrapedtitle = scrapedtitle.replace("-)", ")").replace("’", "'")
        scrapedtitle = scrapedtitle.replace("Streaming", "").replace(":", "")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos_movie" if not "series" in genre else "episodios",
                 contentType="movie",
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=scrapedtitle,
                 plot=scrapedplot,
                 folder=True), tipo='movie' if not "series" in genre else "tv"))

    # Paginación
    next_page = scrapertools.find_single_match(data, '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>')
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_movie",
                 title="[COLOR orange]Successivi >>[/COLOR]",
                 url=next_page,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/next_1.png"))

    return itemlist

# ==================================================================================================================================================

def episodios(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] episodios")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = r'<iframe src="([^"]+)" scrolling="no" frameborder="0" width="626" height="550" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'
    url = scrapertools.find_single_match(data, patron)

    data = httptools.downloadpage(url).data.replace('\n', '')


    section_stagione = scrapertools.find_single_match(data, '<i class="fa fa-home fa-fw"></i> Stagioni</a>(.*?)<select name="sea_select" class="dynamic_select">')
    patron = '<a href="([^"]+)" ><i class="fa fa-tachometer fa-fw"></i>\s*(\d+)</a></li>'
    seasons = re.compile(patron, re.DOTALL).findall(section_stagione)

    for scrapedseason_url, scrapedseason in seasons:

        season_url = urlparse.urljoin(url, scrapedseason_url)
        data = httptools.downloadpage(season_url).data.replace('\n', '')

        section_episodio = scrapertools.find_single_match(data, '<i class="fa fa-home fa-fw"></i> Episodio</a>(.*?)<select name="ep_select" class="dynamic_select">')
        patron = '<a href="([^"]+)" ><i class="fa fa-tachometer fa-fw"></i>\s*(\d+)</a>'
        episodes = re.compile(patron, re.DOTALL).findall(section_episodio)

        for scrapedepisode_url, scrapedepisode in episodes:
            episode_url = urlparse.urljoin(url, scrapedepisode_url)

            title = scrapedseason + "x" + scrapedepisode + "[COLOR  yellow]" + " -- " + "[/COLOR]"

            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     contentType="episode",
                     title=title + item.show,
                     url=episode_url, 
                     fulltitle=title,
                     show=item.show,
                     plot=item.plot,
                     thumbnail=item.thumbnail))


    return itemlist

# ==================================================================================================================================================

def findvideos(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] findvideos")
    encontrados = set()
    itemlist = []

    # Descarga la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    patron = r'</ul>\s*<select  style(.*?)</nav>\s*</div>'
    bloque = scrapertools.find_single_match(data, patron)

    # Extrae las entradas (carpetas)
    patron = '<a class="" href="([^"]+)">\s*([^<]+)</a>'
    server_link = scrapertools.find_multiple_matches(bloque, patron)
    for scrapedurl, scrapedtitle in server_link:
        data = httptools.downloadpage(scrapedurl, headers=headers).data		
        if 'protectlink.stream' in data:
            scrapedcode = scrapertools.find_multiple_matches(data, r'<iframe src=".*?//.*?=([^"]+)"')

            for url in scrapedcode:
              url = url.decode('base64')
              encontrados.add(url)

    if encontrados:
        itemlist = servertools.find_video_items(data=str(encontrados))
        for videoitem in itemlist:
            videoitem.fulltitle = item.fulltitle
            videoitem.show = item.show
            videoitem.title = item.title + '[COLOR orange]' + videoitem.title + '[/COLOR]'
            videoitem.thumbnail = item.thumbnail
            videoitem.plot = item.plot
            videoitem.channel = __channel__

    return itemlist


# ==================================================================================================================================================

def findvideos_movie(item):
    logger.info("[streamondemand-pureita filmsenzalimiti_info] findvideos_movie")

    # Descarga la página
    data = item.extra if item.extra != '' else httptools.downloadpage(item.url, headers=headers).data

    if 'protectlink.stream' in data:
        page_link = scrapertools.find_multiple_matches(data, r'<iframe src="[^=]+=([^"]+)"')
        for url in page_link:
            url = url.decode('base64')
            data += '\t' + url
			
            url = httptools.downloadpage(url, only_headers=True, follow_redirects=False).headers.get("location", "")
            data += '\t' + url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + "[COLOR orange]" + videoitem.title + "[/COLOR]"
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__
		
    patron = r'\{"file":"([^"]+)","type":"[^"]+","label":"([^"]+)"\}'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        title = item.title + " " + scrapedtitle
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl.replace(r'\/', '/').replace('%3B', ';'),
                 thumbnail=item.thumbnail,
                 fulltitle=item.title,
                 show=item.title,
                 server='',
                 folder=False))

    return itemlist

# ==================================================================================================================================================

