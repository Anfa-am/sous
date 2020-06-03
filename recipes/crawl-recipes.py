from __future__ import division
import pymongo
from bson.objectid import ObjectId
import re
from itertools import chain
from quantulum3 import parser
import os
import sys
import json
import pprint
import pdb

connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection["sous"]
recipe_collection = db["recipe"]

recipes = db.recipe.find()

pp = pprint.PrettyPrinter(indent=2)


SEPARATOR_RE = re.compile(r'^([\d\s*[\d\.,/]*)\s*(.+)')


def normalize(st):
    """

    :param st:
    :return:
    """
    return re.sub(r'\s+', ' ', SEPARATOR_RE.sub('\g<1> \g<2>', st)).strip()


def escape_re_string(text):
    """

    :param text:
    :return:
    """
    text = text.replace('.', '\.')
    return re.sub(r'\s+', ' ', text)


UNITS = {"cup": ["cups", "cup", "c.", "c"], "fluid_ounce": ["fl. oz.", "fl oz", "fluid ounce", "fluid ounces"],
         "gallon": ["gal", "gal.", "gallon", "gallons"], "ounce": ["oz", "oz.", "ounce", "ounces"],
         "pint": ["pt", "pt.", "pint", "pints"], "pound": ["lb", "lb.", "pound", "pounds"],
         "quart": ["qt", "qt.", "qts", "qts.", "quart", "quarts"],
         "whole": ["whole"],
         "tablespoon": ["tbsp.", "tbsp", "T", "T.", "tablespoon", "tablespoons", "tbs.", "tbs"],
         "teaspoon": ["tsp.", "tsp", "t", "t.", "teaspoon", "teaspoons"],
         "gram": ["g", "g.", "gr", "gr.", "gram", "grams"], "kilogram": ["kg", "kg.", "kilogram", "kilograms"],
         "liter": ["l", "l.", "liter", "liters"], "milligram": ["mg", "mg.", "milligram", "milligrams"],
         "milliliter": ["ml", "ml.", "milliliter", "milliliters"], "pinch": ["pinch", "pinches"],
         "dash": ["dash", "dashes"], "touch": ["touch", "touches"], "handful": ["handful", "handfuls"],
         "stick": ["stick", "sticks"], "clove": ["cloves", "clove"], "can": ["cans", "can"], "large": ["large"],
         "small": ["small"], "scoop": ["scoop", "scoops"], "filets": ["filet", "filets"], "sprig": ["sprigs", "sprig"]}

NUMBERS = ['seventeen', 'eighteen', 'thirteen', 'nineteen', 'fourteen', 'sixteen', 'fifteen', 'seventy', 'twelve',
           'eleven', 'eighty', 'thirty', 'ninety', 'twenty', 'seven', 'fifty', 'sixty', 'forty', 'three', 'eight',
           'four', 'zero', 'five', 'nine', 'ten', 'one', 'six', 'two', 'an ', 'a ', "½", "↉", "⅓", "⅔", "¼", "¾", "⅕", "⅖", "⅗", "⅘", "⅙", "⅚", "⅐", "⅛", "⅜", "⅝", "⅞", "⅑", "⅒", "⅟"]

prepositions = ["of"]

a = list(chain.from_iterable(UNITS.values()))
a.sort(key=lambda x: len(x), reverse=True)
a = map(escape_re_string, a)

PARSER_RE = re.compile(
    r'(?P<quantity>(?:[\d\.,][\d\.,\s/]*)?\s*(?:(?:%s)\s*)*)?(\s*(?P<unit>%s)\s+)?(\s*(?:%s)\s+)?(\s*(?P<name>.+))?' % (
        '|'.join(NUMBERS), '|'.join(a), '|'.join(prepositions)))


def parse_ingredient(st):
    """

    :param st:
    :return:
    """
    st = normalize(st)
    res = PARSER_RE.match(st)

    name = re.split(', | \(', (res.group('name') or '').strip())

    return {
        'measure': (res.group('quantity') or '').strip(),
        'unit': (res.group('unit') or '').strip(),
        'name': name[0].replace(')', ''),
        'details': list(map(lambda s: s.replace(')', ''), name[1:] ))
        
    }

print('start')
for recipe in recipes:
    if(isinstance(recipe["steps"], str)):
        name = recipe["name"].replace('Recipe', '').strip()
        steps = recipe["steps"].replace("Please enable targetting cookies to show this banner if (window.innerWidth <= 10000 && window.innerWidth >= 768) { propertag.cmd.push(function() { proper_display('jamieoliver_leftrail'); }); }", '').strip()

        steps_array = []

        steps.replace('\n', '')
        steps.replace('40.', '').replace('39.', '').replace('38.', '').replace('37.', '').replace('36.', '').replace('35.', '').replace('34.', '').replace('33.', '').replace('32.', '').replace('31.', '').replace('30.', '').replace('29.', '').replace('28.', '').replace('27.', '').replace('26.', '').replace('25.', '').replace('24.', '').replace('23.', '').replace('22.', '').replace('21.', '').replace('20.', '').replace('19.', '').replace('18.', '').replace('17.', '').replace('16.', '').replace('15.', '').replace('14.', '').replace('13.', '').replace('12.', '').replace('11.', '').replace('10.', '').replace('9.', '').replace('8.', '').replace('7.', '').replace('6.', '').replace('5.', '').replace('4.', '').replace('3.', '').replace('2.', '').replace('1.', '')
        steps = re.sub(r'(\d+)/(\d+)', lambda m: str(int(m.group(1))/int(m.group(2))), steps)

        steps_data = steps.split('.')

        print(recipe["_id"])
        for step in steps_data:
            steps_array.append({
                "text": step.strip(),
                "interpol": parser.inline_parse(step.strip()),
                "quantities": list(map(lambda s: {"value": s.surface, "type": s.unit.name }, parser.parse(step.strip() ) ))
            })

        ings_array = []

        for ing in recipe["ingredients"]:
            hnewIng = ing.replace('-', ' ').strip()
            newIng = re.sub(r'(\d+)/(\d+)', lambda m: str(int(m.group(1))/int(m.group(2))), hnewIng)
            ings_array.append({
                "description" : newIng,
                "interpol" : parser.inline_parse(newIng.strip()),
                "products" : parse_ingredient(newIng),
                "quantities": list(map(lambda s: {"value": s.surface, "type": s.unit.name }, parser.parse(newIng) ))
            })

        if recipe["yeild"]:
            yeild = parser.parse(recipe["yeild"])[0].surface
        else:
            yeild = 'n/a'

        complexity = len(recipe["ingredients"]) * (len(steps) + recipe["time"])

        newData = {
            "name": name,
            "steps": steps_array,
            "yeild": yeild,
            "complexity": complexity,
            "ingredients": ings_array,
        }

        pp.pprint(newData)

        db.recipe.update_one({ '_id': ObjectId(recipe["_id"])}, { '$set': newData }, upsert=False)


# from bs4 import BeautifulSoup
# from recipe_scrapers import scrape_me

# import pymongo
# import requests
# import re
# import urllib.request, urllib.error, urllib.parse
# import os
# import argparse
# import sys
# import json

# connection = pymongo.MongoClient("mongodb://localhost:27017/")
# db = connection["sous"]
# recipe_collection = db["recipe"]

# for dirpath, dirs, files in os.walk('./raw/'):
    # raw_path = dirpath.replace('./raw/','')
    # for f in files:
        # url = 'http://' + raw_path + '/' + f 
        # try:
          # scraper = scrape_me(url)
          # print(url)

          # # replace with new post processing
          # recipe = { 
              # "name": scraper.title(), 
              # "time": scraper.total_time(),
              # "ingredients": scraper.ingredients(),
              # "steps": scraper.instructions(),
              # "yeild": scraper.yields(),
              # "image": scraper.image(),
              # "refDir": scraper.title().lower().replace(" ", "_"),
              # "src": url
           # }

          # recipe_collection.insert_one(recipe)

        # except:
            # print('skip')
