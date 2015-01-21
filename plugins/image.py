#!/usr/bin/python
# -*- coding: utf8 -*-

"""!image/!이미지 <검색 키워드> 이미지를 검색합니다"""

from urllib import quote
import re
import requests
from random import shuffle

def image(searchterm, unsafe=False):
    searchterm = quote(searchterm.encode("utf8"))

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.co.jp/search?tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    images = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(images)

    return images[0] if images else ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:image|이미지) (.*)", text)
    if not match: return

    searchterm = match[0]
    return image(searchterm)
