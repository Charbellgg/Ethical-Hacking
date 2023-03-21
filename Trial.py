import urllib.request
import requests
import re
import sys


def validateUrl(url):

    pattern = r"^((http|https):\/\/)?(www\.)?([\w\-\.]+)+$"
    obj = re.match(pattern, url)
        
    return obj