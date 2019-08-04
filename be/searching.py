from datetime import datetime
from elasticsearch import Elasticsearch
import hashlib
import json
es = Elasticsearch(
    ['https://a925da34d8234304a4c563da5ef21658.asia-northeast1.gcp.cloud.es.io'],
    http_auth=('elastic','EoLRU4zDHbAjG7ELwBXpqOKh'),
    port=9243,
    verify_certs=False
)

query1 = { "query": 
			{ "query_string" : 
				{ "fields" : 
					["storeName", "storeLocation", "productName"],
						"query" : "amul" } 
		} 
	}
	


#query2 = {
#  "query": {
#    "nested": {
#      "path": "products",
#      "query": {
#        {"match": {"products.productName": "Amul"}},
#      },
#	  "score_mode": "avg"
#    }
#  }
#}

#query2 = {'query': {'match': {'storeName': 'more'}}}
#res = json.dumps(query)
#try:
from flask import Flask, request
app = Flask(__name__)

@app.route('/searchProducts', methods=['GET'])
def searchProducts():
	searchString = request.args['searchString']
	query = {
		"query": {
			"nested": {
			  "path": "products",
			  "query": {
				"bool": {
				  "must": [
					{"match": {"products.productName": searchString}},
					{"range": {"products.price": {"gt": 100.0}}}
				  ]
				}
			  },
			  "score_mode": "avg"
			}
		  }
	}
	
	result = es.search(index="store", body=query)
	print(".............\n\n.......\nRes: ",result)
	return result
	
if __name__ == '__main__':
	app.run(host='localhost', debug=True)