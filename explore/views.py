import requests
import time
import base64
import hashlib
import hmac
from urllib import urlencode
from urllib import quote_plus
from django.shortcuts import render
from django.conf import settings


def create_signature_string(params):
    secret = settings.AMAZON_SECRET
    base_url = "http://ecs.amazonaws.com/onca/xml"

    # Add a ISO 8601 compliant timestamp (in GMT)
    params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Sort the URL parameters by key
    keys = params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(params.get, keys)

    # Reconstruct the URL parameters and encode them
    url_string = urlencode(zip(keys, values))

    #Construct the string to sign
    string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string

    # Sign the request
    signature = hmac.new(
        key=secret,
        msg=string_to_sign,
        digestmod=hashlib.sha256).digest()

    # Base64 encode the signature
    signature = base64.encodestring(signature).strip()

    # Make the signature URL safe
    return quote_plus(signature)


def home(request):
    key = settings.AMAZON_KEY
    params = {
        "Service": "AWSECommercService",
        "Operation": "ItemLookup",
        "IdType": "ISBN",
        "ItemId": "9780735619678",
        "SearchIndex": "Books",
        "AWSAccessKeyId": key,
        "ResponseGroup": "Images,ItemAttributes,EditorialReview,SalesRank"
    }
    signature = create_signature_string(params)
    return render(request, 'home.html', {"signature": signature})
