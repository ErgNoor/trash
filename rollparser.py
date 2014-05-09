#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import re


class BaseRollParser(object):
    """docstring for BaseRollParser"""
    def parser(self):
        raise NotImplementedError


class AvtosushiParser(BaseRollParser):
    """docstring for AvtosushiParser"""
    def __init__(self, site, roll_name):
        self.site = site
        # print self.site
        self.roll_name = roll_name

    def parser(self):
        url = "http://www.nn.avtosushi.ru/shop/rolls"
        page = requests.get(url).text.encode("utf-8")

        PRICE_PATTERN = re.compile("\d{2,3}")
        WEIGHT_PATTERN = re.compile("\d{2,4}")
        NAME_PATTERN = re.compile(".* " + self.roll_name + "$")

        doc_page = html.fromstring(page)
        names = doc_page.xpath(".//*[@class='product']//div[@class='hover']//span[@class='name']/text()")
        costs = doc_page.xpath(".//*[@class='product']//div[@class='hover']//div[@class='cost']/text()")
        weights = doc_page.xpath(".//*[@class='product']//div[@class='hover']//span[@class='short']/text()")

        rolls_name = [name.strip() for name in names]
        roll_price = [float(PRICE_PATTERN.search(cost.strip()).group(0)) for cost in costs]
        roll_weight = [float(WEIGHT_PATTERN.search(weight).group(0)) for weight in weights]
        roll_price_unit = [round((price/weight)*100, 2) for (price, weight) in zip(roll_price, roll_weight)]

        roll_params = zip(roll_price, roll_weight, roll_price_unit)
        rolls = dict(zip(rolls_name, roll_params))

        roll = {}
        for name in rolls.keys():
            if NAME_PATTERN.search(name):
                roll = dict(zip((self.roll_name,), (rolls[name],)))
                break

        return roll


class SamurainnParser(BaseRollParser):
    """docstring for SamurainnParser"""
    def __init__(self, site, roll_name):
        self.site = site
        # print self.site
        self.roll_name = roll_name

    def parser(self):
        urls = ("http://samurai-nn.ru/sushi/rolls-complex",
                "http://samurai-nn.ru/sushi/rolls-complex?start=21",
                "http://samurai-nn.ru/sushi/rolls-complex?start=42",
                )
        pages = [requests.get(url).text for url in urls]

        PRICE_PATTERN = re.compile("\d{2,3}")
        WEIGHT_PATTERN = re.compile("(\d{2,4})(.*)")
        NAME_PATTERN = re.compile("^" + self.roll_name + "$")

        rolls = {}

        for page in pages:
            doc_page = html.fromstring(page)
            names = doc_page.xpath(".//*[@class='product']//div[@class='name']/a/text()")
            costs = doc_page.xpath(".//*[@class='product']//div[@class='jshop_price']/text()")
            weights = doc_page.xpath(".//*[@class='product']//div[@class='productweight']/text()")

            rolls_name = [name.strip() for name in names]
            # for name in rolls_name:
            #     print name.encode("utf-8")
            roll_price = [float(PRICE_PATTERN.search(cost.strip()).group(0)) for cost in costs]
            roll_weight = [float(WEIGHT_PATTERN.search(weight.strip()).group(1)) for weight in weights]
            roll_price_unit = [round((price/weight)*100, 2) for (price, weight) in zip(roll_price, roll_weight)]
            roll_params = zip(roll_price, roll_weight, roll_price_unit)

            roll = dict(zip(rolls_name, roll_params))
            rolls.update(roll)

        roll = {}
        for name in rolls.keys():
            if NAME_PATTERN.search(name):
                roll = dict(zip((self.roll_name,), (rolls[name],)))
                break

        return roll


class RollSitesFactory(object):
    """docstring for RollSitesFactory"""
    objects = {
        'avtosushi': AvtosushiParser,
        'samurainn': SamurainnParser,
        'default': AvtosushiParser,
    }

    def get_parser(self, site_name='default', rollname=''):
        return self.objects[site_name](site_name, rollname)


if __name__ == '__main__':
    roll_factory = RollSitesFactory()
    avtosushi = roll_factory.get_parser('avtosushi', u"Филадельфия")
    samurainn = roll_factory.get_parser('samurainn', u"Филадельфия")
    print avtosushi.parser()
    print samurainn.parser()
