import re
import json
import io
import numpy as np
import argparse
import cv2
from PIL import Image
from pytesseract import *
import os


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


def parse_text(str):
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
    
    print(shopName)
    print(gstin)
    print(packingCharges)
    
    
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
    app_json = json.dumps(appDict)
    print(app_json)
    return app_json