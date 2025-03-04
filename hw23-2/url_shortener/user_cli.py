""" URL Shortener API - a bit like bitly"""
# Takes user input URL and converts to short version
# Shor version can be retrieved as original (for redirect)
# see also : pip install short_url if you want to *cheat*

import re
import sys
import json
import socket
import requests


print("."*20)
print("-"*2 + " URL Shortener " + "-"*2)
print("."*20 + "\n")

# API Endpoint to shorten URL
PREFIX_URL = "http://127.0.0.1:8000/api-1.0/"

# Check if server is running
def is_open(server_ip,port):
    """ Check gunicorn is up """
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sckt.connect((server_ip, int(port)))
        sckt.shutdown(2)
        return True
    except ConnectionError :
        return False

if not is_open("127.0.0.1",8000):
    print("Server Not Running - Start gunicorn first '$./server.sh'\n ")
    sys.exit()


# Ask user for a valid http(s) URL to shorten
def user_input()->str:
    """ Ask user for long URL and validate with regex """
    valid = False
    while not valid:
        user_url = input("Enter a url to shorten and press ENTER\n")
        reg_ex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(reg_ex,user_url)
        if not url:
            print("Not a Valid URL")
        else:
            valid = True
    return user_url

# Main Driver

if __name__=="__main__":


    # User's long URL to shorten
    input_url = user_input()

    # Call API
    # Request shortened version from endopoint and display back on CLI
    payload = {'input_url': input_url}
    response = requests.post(PREFIX_URL + "create-short/", params=payload)
    json_data = response.json()
    print(f"\nShortened URL =  {json_data['short_url']}\n")

    # Store the response short url and original long url in a dictionary
    short_url = json_data['short_url']
    dictionary = {
        "short_url": short_url,
        "long_url": input_url,
    }

    # Serializing dictionary as json to write to JSON file
    json_object = json.dumps(dictionary)

    # Write to jsonfile
    with open("map_urls.json","a", encoding="utf-8") as outfile:
        outfile.write(json_object)
        outfile.write('\n')

    # Ask user for a short link to visit - can be a previous one
    to_visit = input(">>> Enter Short URL to visit and press ENTER <<<\n")
    print(f"\nYou want to visit {to_visit}, \nrequesting via the full link: ")


    # Call API - retrive long url from JSON match on short url
    payload = {'short_url': to_visit}
    response = requests.get(PREFIX_URL+"visit-short/",params=payload)
    response = (response.content)

    # print with decode to remove the b'
    print(f"Here is your original, LONGER url :\n\n {response.decode('utf-8')}\n")
    
