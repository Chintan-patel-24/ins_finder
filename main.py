import sys
import colorama
import time
import argparse
import json
import httpx
import hmac
import hashlib
import urllib
import requests
from httpx import get
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init


colorama.init(autoreset=True)


def banner():
    print("                _ _   _                ")
    print("  _  _ ___ ___ (_) |_( )___  _ __  ___ ")
    print(" | || / -_|_-< | |  _|/(_-< | '  \/ -_)")
    print("  \_, \___/__/ |_|\__| /__/ |_|_|_\___|")
    print("  |__/                                 ")
    print("\n\tTwitter: " + Fore.MAGENTA + "@blackeko5")


def getUserId(username, sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
    r = get('https://www.instagram.com/{}/?__a=1'.format(username),
            headers=headers, cookies=cookies)
    try:
        info = json.loads(r.text)
        id = info["logging_page_id"].strip("profilePage_")
        return({"id": id, "error": None})
    except:
        return({"id": None, "error": "User not found or rate limit"})


def getInfo(username, sessionId):
    userId = getUserId(username, sessionId)
    if userId["error"] != None:
        return({"user": None, "error": "User not found or rate limit"})
    else:
        cookies = {'sessionid': sessionId}
        headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
        response = get('https://i.instagram.com/api/v1/users/' +
                       userId["id"]+'/info/', headers=headers, cookies=cookies)
        info = json.loads(response.text)
        infoUser = info["user"]
        infoUser["userID"] = userId["id"]
        return({"user": infoUser, "error": None})

def advanced_lookup(username):
    USERS_LOOKUP_URL = 'https://i.instagram.com/api/v1/users/lookup/'
    SIG_KEY_VERSION = '4'
    IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

    def generate_signature(data):
        return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)

    def generate_data(phone_number_raw):
        data = {'login_attempt_count': '0',
                'directly_sign_in': 'true',
                'source': 'default',
                'q': phone_number_raw,
                'ig_sig_key_version': SIG_KEY_VERSION
                }
        return data

    data = generate_signature(json.dumps(generate_data(username)))
    headers = {
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 101.0.0.15.120",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "X-FB-HTTP-Engine": "Liger",
        "Connection": "close"}
    try:
        r = httpx.post(USERS_LOOKUP_URL, headers=headers, data=data)
        rep = r.json()
        return({"user": rep, "error": None})
    except:
        return({"user": None, "error": "rate limit"})


def dumpor(name):
    url = "https://dumpor.com/search?query="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    req = url + name.replace(" ", "+")

    try:
        account_list = []
        response = requests.get(req, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        accounts = soup.findAll('a', {"class": "profile-name-link"})
        for account in accounts:
            account_list.append(account.text)
        return({"user": account_list, "error": None})
    except:
        return({"user": None, "error": "rate limit"})
