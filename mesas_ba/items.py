# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Seccion(scrapy.Item):
    numero = scrapy.Field()
    nombre = scrapy.Field()

    def __str__(self):
        return f"{self['numero']}- {self['nombre']}"


class Circuito(scrapy.Item):
    seccion = scrapy.Field()
    numero = scrapy.Field()


class Mesa(scrapy.Item):
    # define the fields for your item here like:
    numero = scrapy.Field()
    circuito = scrapy.Field()
    url = scrapy.Field()
    fake_id =scrapy.Field()


class Resultado(scrapy.Item):
    mesa = scrapy.Field()
    partido = scrapy.Field()
    lista = scrapy.Field()
    categoria = scrapy.Field()
    votos = scrapy.Field()


