from __future__ import division
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin



from bs4 import BeautifulSoup

from recipe_scrapers import scrape_me

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pymongo

from bson.objectid import ObjectId
from itertools import chain
from quantulum3 import parser

import io
import os
import sys
import json
import requests
import re
import hashlib
import urllib.request, urllib.error, urllib.parse
from PIL import Image
from libsvm import svmutil
import brisque
import pytesseract
from shutil import rmtree
import time
from pyvirtualdisplay import Display

import concurrent.futures

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import tflearn
import tensorflow as tf
import pickle


connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection["sous"]
recipe_collection = db["recipe"]


client = pymongo.MongoClient("mongodb://localhost:27017/")

display = Display(visible=0, size=(1024, 768))
display.start()

driver_path = "/home/anfa/Downloads/chromedriver"
wd = webdriver.Chrome(executable_path=driver_path)

SEPARATOR_RE = re.compile(r'^([\d\s*[\d\.,/]*)\s*(.+)')

ERROR_THRESHOLD = 0.25

b = brisque.BRISQUE()

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q={q}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga,itp:photo,ic:color,ift:jpg"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < max_links_to_fetch:
        # scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls

            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=100)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

with tf.Graph().as_default():
    types_data = pickle.load( open( "./training/models/types/types", "rb" ) )
    types_words = types_data['words']
    types_classes = types_data['classes']
    types_train_x = types_data['train_x']
    types_train_y = types_data['train_y']

    type_net = tflearn.input_data(shape=[None, len(types_train_x[0])])
    type_net = tflearn.fully_connected(type_net, 8)
    type_net = tflearn.fully_connected(type_net, 8)
    type_net = tflearn.fully_connected(type_net, len(types_train_y[0]), activation='softmax')
    type_net = tflearn.regression(type_net)

    types_model = tflearn.DNN(type_net, tensorboard_dir='./training/models/types/')
    types_model.load('./training/models/types/types.tflearn')

def eval_types(sentence):
    results = types_model.predict([bow(sentence, types_words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((types_classes[r[0]], r[1]))
    return return_list



with tf.Graph().as_default():
    temps_data = pickle.load( open( "./training/models/temps/temps", "rb" ) )
    temps_words = temps_data['words']
    temps_classes = temps_data['classes']
    temps_train_x = temps_data['train_x']
    temps_train_y = temps_data['train_y']

    temp_net = tflearn.input_data(shape=[None, len(temps_train_x[0])])
    temp_net = tflearn.fully_connected(temp_net, 8)
    temp_net = tflearn.fully_connected(temp_net, 8)
    temp_net = tflearn.fully_connected(temp_net, len(temps_train_y[0]), activation='softmax')
    temp_net = tflearn.regression(temp_net)

    temps_model = tflearn.DNN(temp_net, tensorboard_dir='./training/models/temps/')
    temps_model.load('./training/models/temps/temps.tflearn')

def eval_temps(sentence):
    results = temps_model.predict([bow(sentence, temps_words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((temps_classes[r[0]], r[1]))
    return return_list



with tf.Graph().as_default():
    courses_data = pickle.load( open( "./training/models/courses/courses", "rb" ) )
    courses_words = courses_data['words']
    courses_classes = courses_data['classes']
    courses_train_x = courses_data['train_x']
    courses_train_y = courses_data['train_y']

    courseNet = tflearn.input_data(shape=[None, len(courses_train_x[0])])
    courseNet = tflearn.fully_connected(courseNet, 8)
    courseNet = tflearn.fully_connected(courseNet, 8)
    courseNet = tflearn.fully_connected(courseNet, len(courses_train_y[0]), activation='softmax')
    courseNet = tflearn.regression(courseNet)

    courses_model = tflearn.DNN(courseNet, tensorboard_dir='./training/models/courses/')
    courses_model.load('./training/models/courses/courses.tflearn')

def eval_courses(sentence):
    results = courses_model.predict([bow(sentence, courses_words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((courses_classes[r[0]], r[1]))
    return return_list



with tf.Graph().as_default():
    cusines_data = pickle.load( open( "./training/models/cusines/cusines", "rb" ) )
    cusines_words = cusines_data['words']
    cusines_classes = cusines_data['classes']
    cusines_train_x = cusines_data['train_x']
    cusines_train_y = cusines_data['train_y']

    cusineNet = tflearn.input_data(shape=[None, len(cusines_train_x[0])])
    cusineNet = tflearn.fully_connected(cusineNet, 8)
    cusineNet = tflearn.fully_connected(cusineNet, 8)
    cusineNet = tflearn.fully_connected(cusineNet, len(cusines_train_y[0]), activation='softmax')
    cusineNet = tflearn.regression(cusineNet)

    cusines_model = tflearn.DNN(cusineNet, tensorboard_dir='./training/models/cusines/')
    cusines_model.load('./training/models/cusines/cusines.tflearn')

def eval_cusines(sentence):
    results = cusines_model.predict([bow(sentence, cusines_words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((cusines_classes[r[0]], r[1]))
    return return_list

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

app = Flask(__name__)
cors = CORS(app)

@app.route('/oneshot', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def import_recipe():
    data = json.loads(request.data)
    url = data.get("url")
    id = data.get("id")

    scraper = scrape_me(url)
    recipe = {
          "name": scraper.title(),
          "time": scraper.total_time(),
          "ingredients": scraper.ingredients(),
          "steps": scraper.instructions(),
          "yeild": scraper.yields(),
          "image": scraper.image(),
          "refDir": scraper.title().lower().replace(" ", "_"),
          "src": url,
          "addedBy": id,
        }

    name = recipe["name"].replace('Recipe', '').strip()
    steps = recipe["steps"].replace("Please enable targetting cookies to show this banner if (window.innerWidth <= 10000 && window.innerWidth >= 768) { propertag.cmd.push(function() { proper_display('jamieoliver_leftrail'); }); }", '').strip()

    steps_array = []

    steps.replace('\n', '')
    steps.replace('40.', '').replace('39.', '').replace('38.', '').replace('37.', '').replace('36.', '').replace('35.', '').replace('34.', '').replace('33.', '').replace('32.', '').replace('31.', '').replace('30.', '').replace('29.', '').replace('28.', '').replace('27.', '').replace('26.', '').replace('25.', '').replace('24.', '').replace('23.', '').replace('22.', '').replace('21.', '').replace('20.', '').replace('19.', '').replace('18.', '').replace('17.', '').replace('16.', '').replace('15.', '').replace('14.', '').replace('13.', '').replace('12.', '').replace('11.', '').replace('10.', '').replace('9.', '').replace('8.', '').replace('7.', '').replace('6.', '').replace('5.', '').replace('4.', '').replace('3.', '').replace('2.', '').replace('1.', '')
    steps = re.sub(r'(\d+)/(\d+)', lambda m: str(int(m.group(1))/int(m.group(2))), steps)

    steps_data = steps.split('.')

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

    recipe["name"] = name
    recipe["steps"] = steps_array
    recipe["yeild"] = yeild
    recipe["complexity"] = complexity
    recipe["ingredients"] = ings_array

    name = recipe["name"].strip()
    steps = recipe["steps"]

    eval_string = recipe["name"] + ': ' + '. '.join(list(map(lambda s: s["text"], recipe["steps"])))

    type_perdiction = eval_types(eval_string)
    if(type_perdiction and type_perdiction[0][1] > 0.25):
        type_intent = type_perdiction[0][0]
    else:
        type_intent = 'n/a'

    cusine_perdiction = eval_cusines(eval_string)
    if(cusine_perdiction and cusine_perdiction[0][1] > 0.25):
        cusine_intent = cusine_perdiction[0][0]
    else:
        cusine_intent = 'n/a'

    course_perdiction = eval_courses(eval_string)
    if(course_perdiction and course_perdiction[0][1] > 0.25):
        course_intent = course_perdiction[0][0]
    else:
        course_intent = 'n/a'

    temp_perdiction = eval_temps(eval_string)
    if(temp_perdiction and temp_perdiction[0][1] > 0.25):
        temp_intent = temp_perdiction[0][0]
    else:
        temp_intent = 'n/a'


    recipe["classification"] = {
        "type": type_intent,
        "course": course_intent,
        "cusine": cusine_intent,
        "temp": temp_intent
    }

    r = recipe_collection.insert_one(recipe)

    print(r.inserted_id)

    base = '/run/media/anfa/1C8A5B0249DD18B9/h32/'
    target_folder = base + str(r.inserted_id)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

        with webdriver.Chrome(executable_path=driver_path) as wd:
            name = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,']", "", recipe["name"].strip())
            res = fetch_image_urls(name, 10, wd=wd)

        if not res is None:
            for elem in res:
                persist_image(target_folder,elem)

            for dirpath, dirs, files in os.walk(target_folder):
                fs = files
                scores = []
                raw_scores = []
                position = 0

                if files:
                    for f in fs:
                        if f != 'hold':
                            path = dirpath + '/' + f
                            img = Image.open(path)
                            width, height = img.size

                            if int(width) > 600 and int(height) > 600:
                                if pytesseract.image_to_string(img):
                                    os.remove(path)
                                else:
                                    score = b.get_score(path)
                                    if score > 34.5:
                                        scores.append({ "file": f, "score": score })
                                        raw_scores.append(score)
                                        print(score)
                                    else:
                                        os.remove(path)
                            else:
                                os.remove(path)

                    order = sorted(scores, key = lambda i: i['score'], reverse=True)

                    for score in order:
                        path = dirpath + '/' + score["file"]
                        os.rename(path, dirpath + '/' + str(position) + ".jpg")
                        position = position + 1

                    if scores:
                        avg = sum(raw_scores)/len(raw_scores)
                    else:
                        avg = 0

                    db.recipe.update_one({ '_id': r.inserted_id },{
                      '$set': {
                        'analytics': {
                            'veiws': 0,
                            'likes': 0,
                            'shares': 0,
                            'saves': 0,
                            'cooks': 0,
                            'aesthtetic': avg,
                        }
                      }
                    }, upsert=False)

                    res = make_response(jsonify({'done': True, 'id': str(r.inserted_id)}), 200)
                    return res
