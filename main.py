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

