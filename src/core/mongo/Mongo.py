#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import Item, Field


class Mongo(Item):

    # mongo主键
    _id = Field()