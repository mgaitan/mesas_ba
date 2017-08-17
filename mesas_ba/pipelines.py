# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from .items import Seccion, Circuito, Mesa, Resultado


class CsvPipeline(object):
    def __init__(self):
        self.files = {
            Seccion: open("secciones.csv", 'wb'),
            Circuito: open("circuitos.csv", 'wb'),
            Mesa: open('mesas.csv', 'wb'),
            Resultado: open('resultados.csv', 'wb')
        }
        self.exporters = {k: CsvItemExporter(v) for k, v in self.files.items()}
        for exporter in self.exporters.values():
            exporter.start_exporting()

    def close_spider(self, spider):
        for k in (Seccion, Circuito, Mesa, Resultado):
            self.exporters[k].finish_exporting()
            self.files[k].close()

    def process_item(self, item, spider):
        self.exporters[type(item)].export_item(item)
        return item
