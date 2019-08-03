from datetime import datetime
from elasticsearch import Elasticsearch
import hashlib
es = Elasticsearch(
    ['https://a925da34d8234304a4c563da5ef21658.asia-northeast1.gcp.cloud.es.io'],
    http_auth=('elastic','EoLRU4zDHbAjG7ELwBXpqOKh'),
    port=9243,
    verify_certs=False
)

stringToHash = 'More Megastore ' + 'Bellandur'

#converting to lowercase alpha characters only (no spaces, no special characters)
stringToHash = ''.join(filter(str.isalpha, stringToHash))
stringToHash = stringToHash.lower()
print("stringToHash: ",stringToHash,"\n\n\n")

hash_object = hashlib.md5(stringToHash.encode())
hashedId = hash_object.hexdigest()
print(hashedId)

doc = {
    'storeName': 'More Megastore',
    'storeLocation': 'Bellandur',
    'timestamp': datetime.now(),
    'gstNumber': '12343874',
    'storeImgLocation': 'http://morestore.com/Content/CategoryImages/quality1st_homepage_banners.jpg',
    'products': [
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
#res = es.index(index="stores", doc_type='stores', id=1, body=doc)
#print(res['result'])





#Retrieving the existing list
res = ""
try:
    res = es.get(index="stores", doc_type='stores', id=hashedId)
    storeData = res['_source']
    print("store data: ",storeData)

    #List exists.. Append to the Array
    productList = storeData['products']
    print("product list: ",productList)
    productList.append({
        'productName': 'Item A',
        'price': 10.0,
        'productImgLocation': 'https://4.imimg.com/data4/TP/FJ/ANDROID-17923575/product-250x250.jpeg'
    })
    print("\n\nfinal product list: ",productList)
    storeData['products'] = productList
    print("\n\nfinal store data: ", storeData)
    es.index(index="stores", doc_type='stores', id=hashedId, body=storeData)
    print("Data store success.............")
except:
    if '_source' not in res:
        print("got 404..hahaha....")

#res = es.search(index = "stores", body={"query": {"match": {"_id": 21442342}}})

es.indices.refresh(index="stores")

#res = es.search(index="stores", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total']['value'])
#print("res: ",res)
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(stores)s: %(text)s" % hit["_source"])