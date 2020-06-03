import pymongo
from bson.objectid import ObjectId
import os
import argparse
import sys
import json
from libsvm import svmutil
import brisque
import PIL.Image
import pytesseract
from shutil import rmtree

connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection["sous"]
recipe_collection = db["recipe"]

target_folder = '/run/media/anfa/1C8A5B0249DD18B9/h32/' 
b = brisque.BRISQUE()

for dirpath, dirs, files in os.walk(target_folder):
    for di in dirs:
        for dirpath, dirs, files in os.walk(target_folder + di):
            fs = files
            scores = []
            raw_scores = []
            position = 0 

            if files:
                for f in fs:
                    if f != 'hold':
                        path = dirpath + '/' + f
                        img = PIL.Image.open(path)
                        width, height = img.size

                        print(f)
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
                    print(dirpath)
                    rmtree(dirpath, ignore_errors=True)
                    avg = 0

                db.recipe.update_one({ '_id': ObjectId(di) },{
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

            else: 
                os.rmdir(dirpath)
