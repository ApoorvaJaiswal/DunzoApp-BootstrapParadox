#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 08:08:37 2019

@author: ashrafaliansari
"""

import flask
from datetime import datetime



import json
import re
str = 'Leon Grill\nIndfra Nagar 80ft Road\nPhone:7676100700\nAlternate Phone:8951085615\nTin No: 29591259669\nDate:21-2-2017 8:26 pm\nSerial No: 199\nSale Type: Take-away\nQty Total\nItem Name\n4 Pc Hot&Spicy Chicken\n280\n240\nChicken Doner Pitta/Hummus 2\nTotal Bill:\nTakeAway Charges:\nAmount to be paid:\n520.00\n20.00\n540.00\nThank You...! Visit again\n'
gstinRegex = re.compile(r'tin no.*(\d{11})',re.I)
shopNameRegex = re.compile(r'\s*(.*)\S')
match = gstinRegex.search(str)
gstin = match.group(1)
match = shopNameRegex.search(str)
shopName = match.group(0)
doc = {
  'gstNumber': gstin,
  'storeName':shopName,
  'storeLocation': 'bellandur',
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

#ASH

#print("gstNumber: ",doc['gstNumber'],".......")
#stringToHash = 'More Megastore ' + 'banshankari'
#stringToHash = doc['gstNumber']

#converting to lowercase alpha characters only (no spaces, no special characters)
#stringToHash = ''.join(filter(str.isalpha, stringToHash))
#stringToHash = stringToHash.lower()
#print("stringToHash: ",stringToHash,"\n\n\n")

#hash_object = hashlib.md5(stringToHash.encode())
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






