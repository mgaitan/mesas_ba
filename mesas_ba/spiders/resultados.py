# -*- coding: utf-8 -*-
from itertools import product
import scrapy
from pyquery import PyQuery
from ..items import Seccion, Circuito, Mesa, Resultado

BASE = 'http://www.resultados.gob.ar/99/resu/content/telegramas/'

def get_links(response, url):
    base_url = url.rpartition('/')[0] + '/'
    pq = PyQuery(response.text)
    pq.make_links_absolute(base_url=base_url)
    links = [pq(a) for a in pq('li a')]
    return {a.text().strip(): a.attr('href') for a in links}


class ResultadosSpider(scrapy.Spider):
    name = 'resultados'
    # allowed_domains = ['http://www.resultados.gob.ar']
    start_urls = [f'{BASE}IMUN02.htm']

    def parse(self, response):
        secciones = get_links(response, url=response.url)
        for text, url in secciones.items():
            numero, nombre = text.strip().split(' - ')
            yield Seccion(numero=numero, nombre=nombre)
            yield scrapy.Request(url, callback=self.parse_circuitos, meta={'seccion': numero})

    def parse_circuitos(self, response):
        seccion = response.meta['seccion']
        circuitos = get_links(response, url=response.url)
        for text, url in circuitos.items():
            circuito = Circuito(numero=text, seccion=seccion)
            yield circuito
            request = scrapy.Request(url, callback=self.parse_mesas)
            request.meta['circuito'] = circuito['numero']
            yield request

    def parse_mesas(self, response):
        circuito = response.meta['circuito']
        mesas = get_links(response, url=response.url)
        for text, url in mesas.items():

            mesa = Mesa(numero=text, circuito=circuito, fake_id=f'{circuito}-{text}', url=url.replace(BASE, ''))
            yield mesa
            request = scrapy.Request(url, callback=self.parse_resultados)
            request.meta['mesa'] = mesa['fake_id']
            yield request

    def parse_resultados(self, response):
        pq = PyQuery(response.text)
        mesa = response.meta['mesa']
        senadores = {}
        diputados = {}
        tipo = ['nulos', 'blancos', 'recurridos']
        categorias = ['sen', 'dip']
        votos = pq('div.pt1 tbody td:lt(2)').text().split()
        for (tipo, cat), vot in zip(product(tipo, categorias), votos):
            yield Resultado(partido=tipo, categoria=cat, votos=vot, mesa=mesa)
        impuganados = pq('div.pt2 td').text()
        for cat in categorias:
            yield Resultado(partido='impuganados', categoria=cat, votos=impuganados, mesa=mesa)

        filas = pq('#TVOTOS tr')

        partido = None
        resultados = {}
        for fila in filas:
            fila = pq(fila)
            if fila.text().startswith('Agrupaciones'):
                continue

            new_partido = fila.children('th.alaizquierda').text()
            if new_partido:
                partido = new_partido
                continue
            children = fila.children()
            if children:
                lista, vot_sena, vot_dipu = [td.text for td in children[:3]]
                if vot_sena != '\xa0':
                    yield Resultado(partido=partido, lista=lista, categoria='sen', votos=vot_sena, mesa=mesa)
                if vot_dipu != '\xa0':
                    yield Resultado(partido=partido, lista=lista, categoria='dip', votos=vot_dipu, mesa=mesa)








