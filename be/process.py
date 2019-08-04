import re
import json
import io
import numpy as np
import argparse
import cv2
from PIL import Image
from pytesseract import *
import os
import flask
from datetime import datetime

from elasticsearch import Elasticsearch
import hashlib
es = Elasticsearch(
    ['https://a925da34d8234304a4c563da5ef21658.asia-northeast1.gcp.cloud.es.io'],
    http_auth=('elastic','EoLRU4zDHbAjG7ELwBXpqOKh'),
    port=9243,
    verify_certs=False
)

def parse_image(image_path=None):
    """
    Parse the image using Google Cloud Vision API, Detects "document" features in an image
    :param image_path: path of the image
    :return: text content
    :rtype: str
    """

    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=open(image_path, 'rb'))
    text = response.text_annotations
    del response

    return text[0].description


def parse_text(str=none):
    gstinRegex = re.compile(r'tin no.*(\d{11})',re.I)
    shopNameRegex = re.compile(r'\s*(.*)\S')
    packingChargeRegex = re.compile(r'((TakeAway|Delivery) Charges)[:-]\s*(\d*)\S',re.I)
    
    match = gstinRegex.search(str)
    if match is not None:
        gstin = match.group(1)
    
    match = shopNameRegex.search(str)
    if match is not None:
        shopName = match.group(0)
    
    match = packingChargeRegex.search(str)
    if match is not None:
        packingCharges = match.group(3)
    
    #print(shopName)
    #print(gstin)
    #print(packingCharges)
    
    
    appDict = {
      'GSTIN': gstin,
      'Store Name':shopName,
      'products': [
            {
                'productName': 'Kissan Ketchup 200g',
                'price': 250.0         
            },
            {
                'productName': 'Nescafe Coffee Powder 500g',
                'price': 400.0
            },
            {
                'productName': 'Amul Chocolate',
                'price': 150.0
            }
        ]
    }
    #app_json = json.dumps(appDict)
    #print(app_json)
    return appDict

def elasticSearch(doc):
    hashedId = doc['gstNumber']
    print(hashedId)
    
    mapping = {
        "mappings": {
            "properties" : {
                "storeName": { "type": "text"  },
                "storeLocation": { "type": "text"  },
                "timestamp": { "type": "date"  },
                "gstNumber": { "type": "text"  },
                "products" : {
                    "type" : "nested",
                    "properties": {
                        "productName":    { "type": "text"  },
                        "price": { "type": "float"  }
                    }
                }
            }
        }
    }
    
    doc1 = {
        'storeName': 'More Megastore',
        'storeLocation': 'banshankari',
        'timestamp': datetime.now(),
        'gstNumber': '12343874',
        'products':[
            {
                'productName': 'Kissan Ketchup 200g',
                'price': 250.0,
                'productImgLocation': 'https://images-na.ssl-images-amazon.com/images/I/61JrHlMHF3L._SX679_.jpg'
            },
            {
                'productName': 'Nescafe Coffee Powder 500g',
                'price': 400.0,
                'productImgLocation': 'https://c.ndtvimg.com/2019-03/89f6dc5_coffee_625x300_15_March_19.jpg'
            },
            {
                'productName': 'Amul Chocolate',
                'price': 150.0,
                'productImgLocation': 'https://4.imimg.com/data4/TP/FJ/ANDROID-17923575/product-250x250.jpeg'
            }
        ]
    }
    #res = es.index(index="store", doc_type='store', id=1, body=doc)
    #print(res['result'])
    
    
    if not es.indices.exists(index="store"):
        es.indices.create(index="store", body=mapping)
        created = True
        print('Created Index')
    
    
    #Retrieving the existing list
    res = ""
    try:
        res = es.get(index="store", doc_type='store', id=hashedId)
        storeData = res['_source']
        print("store data: ",storeData)
    
        #List exists.. Append to the Array
        productList = storeData['products']
        newProductList = doc['products']
        print("product list: ",productList)
        productList.append(newProductList)
        print("\n\nfinal product list: ",productList)
        storeData['products'] = productList
        print("\n\nfinal store data: ", storeData)
        es.index(index="store", id=hashedId, body=storeData)
        print("Data store success.............")
    except:
        if '_source' not in res:
            print("got 404..hahaha....")
            outcome = es.index(index="store", id=hashedId, body=doc)
            print(outcome)
    
    #res = es.search(index = "store", body={"query": {"match": {"_id": 21442342}}})
    
    es.indices.refresh(index="store")
    
    #res = es.search(index="store", body={"query": {"match_all": {}}})
    #print("Got %d Hits:" % res['hits']['total']['value'])
    #print("res: ",res)
    #for hit in res['hits']['hits']:
    #    print("%(timestamp)s %(store)s: %(text)s" % hit["_source"])
    
    
    
    
    print("Success")






app = Flask(__name__)

@app.route('/back')
def be():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    #to do call parse_image after saving the np image to image
    #str = parse_image(image)
    str = 'Leon Grill\nIndfra Nagar 80ft Road\nPhone:7676100700\nAlternate Phone:8951085615\nTin No: 29591259669\nDate:21-2-2017 8:26 pm\nSerial No: 199\nSale Type: Take-away\nQty Total\nItem Name\n4 Pc Hot&Spicy Chicken\n280\n240\nChicken Doner Pitta/Hummus 2\nTotal Bill:\nTakeAway Charges:\nAmount to be paid:\n520.00\n20.00\n540.00\nThank You...! Visit again\n'
    doc = parse_text(str)
    elasticSearch(doc)

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    # start flask app
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)