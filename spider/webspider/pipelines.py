# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.update_by_query import UpdateByQuery

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class WebspiderPipeline(object):

    def open_spider(self, spider):
        self.client = Elasticsearch()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        doc = {}

        item
        url = item["url"]
        snapshot = item["snapshot"]
        doc["url"] = url
        doc["snapshot"] = [snapshot]
        try:
            self.client.create(index="website", id=url, body=doc)
        except:
            query={
                "script": {
                    "source": "ctx._source.snapshot.add(params.snapshot)",
                    "lang": "painless",
                    "params": {
                        "snapshot": snapshot
                    }
                }
            }
            self.client.update(index="website", doc_type="_doc", id=url, body=query)
        return item
