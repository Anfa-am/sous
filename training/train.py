import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import pymongo
import numpy as np
import tflearn
import tensorflow as tf

import random
import json
import pickle

ignore_words = ['?', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.', '21.', '22.', '23.', '24.', '25.', '26.', '27.', '28.', '29.', '30.', '31.', '32.', '33.', '34.', '35.', '36.', '37.', '38.', '39.', '40.',]

def train_temps():
    with open('./temps.json') as json_data:
        intents = json.load(json_data)
        words = []
        classes = []
        documents = []

        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = nltk.word_tokenize(pattern)
                # add to our words list
                words.extend(w)
                # add to documents in our corpus
                documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        training = []
        output = []
        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:,0])
        train_y = list(training[:,1])

        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir='./models/temps/logs/')
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

        model.save('./models/temps/temps.tflearn')

        pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "./models/temps/temps", "wb" ) )

def train_cusines():
    with open('./cusines.json') as json_data:
        intents = json.load(json_data)
        words = []
        classes = []
        documents = []

        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = nltk.word_tokenize(pattern)
                # add to our words list
                words.extend(w)
                # add to documents in our corpus
                documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        training = []
        output = []
        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:,0])
        train_y = list(training[:,1])

        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir='./models/cusines/logs/')
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

        model.save('./models/cusines/cusines.tflearn')

        pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "./models/cusines/cusines", "wb" ) )

def train_courses():
    with open('./courses.json') as json_data:
        intents = json.load(json_data)
        words = []
        classes = []
        documents = []

        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = nltk.word_tokenize(pattern)
                # add to our words list
                words.extend(w)
                # add to documents in our corpus
                documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        training = []
        output = []
        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:,0])
        train_y = list(training[:,1])

        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir='./models/courses/logs/')
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

        model.save('./models/courses/courses.tflearn')

        pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "./models/courses/courses", "wb" ) )

def train_types():
    with open('./types.json') as json_data:
        intents = json.load(json_data)
        words = []
        classes = []
        documents = []

        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = nltk.word_tokenize(pattern)
                # add to our words list
                words.extend(w)
                # add to documents in our corpus
                documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        training = []
        output = []
        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:,0])
        train_y = list(training[:,1])

        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir='./models/types/logs')
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

        model.save('./models/types/types.tflearn')

        pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "./models/types/types", "wb" ) )

def spit():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sous"]
    recipes = db.recipe.aggregate([{'$sample': {'size': 500 }}], allowDiskUse=True)
    i =  0

    typeHold = []
    cusineHold = []
    seasonHold = []
    courseHold = []

    for r in recipes:
        if i < 100:
            typeHold.append(r["name"] + ': ' + r["steps"].replace('\n', ''))


        if i > 100 and i < 200:
            seasonHold.append(r["name"] + ': ' + r["steps"].replace('\n', ''))

        if i > 300 and i < 400:
            cusineHold.append(r["name"] + ': ' + r["steps"].replace('\n', ''))

        if i > 400 and i < 500:
            courseHold.append(r["name"] + ': ' + r["steps"].replace('\n', ''))

        i = i + 1

    with open('types.txt', 'w') as f:
        for item in typeHold:
            f.write(item)
            f.write("\n")

    with open('temps.txt', 'w') as f:
        for item in seasonHold:
            f.write(item)
            f.write("\n")

    with open('cusines.txt', 'w') as f:
        for item in cusineHold:
            f.write(item)
            f.write("\n")

    with open('courses.txt', 'w') as f:
        for item in courseHold:
            f.write( item)
            f.write("\n")

def train():
    train_cusines()
    train_courses()
    train_types()
    train_temps()

train()
