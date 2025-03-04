""" URL Shortener API """
from random import choice
import string
from urllib.parse import urlparse
import json

# Create random alphanumeric to append to scheme + netloc
def gen_short_url(num_of_chars: int)->str:
    """ Generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

# Chop up the URL into just scheme + netloc
def parse_base_url(starting_url : str)->str:
    """ Extract the hostname from the URL """
    sections = urlparse(starting_url)
    shorter_url =(sections.scheme + "://" + sections.netloc)
    return shorter_url

# Load JSON file find the matching longer URL
def json_url_lookup(short_url:str)->str:
    """Function to return the longer url from the shorter url"""
    dct = [json.loads(line) for line in open("map_urls.json","r",encoding="utf-8")
        if short_url in line]
    long_url = (dct[0]['long_url'])
    return long_url
