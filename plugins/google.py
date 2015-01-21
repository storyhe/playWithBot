#!/usr/bin/python
# -*- coding: utf8 -*-

"""!search/!gg/!google <키워드>; 키워드를 검색합니다."""
from bs4 import BeautifulSoup
import re
from urllib import quote, unquote
import requests

def google(q):
    query = quote(q).encode("utf8")
    url = "https://encrypted.google.com/search?q={0}".format(query)
    soup = BeautifulSoup(requests.get(url.encode("utf8")).text)

    answer = soup.findAll("h3", attrs={"class": "r"})
    if not answer:
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])

def on_message(msg, server):
    text = msg.get("text", "").encode("utf8")
    match = re.findall(r"!(?:google|gg|search) (.*)", text)
    if not match: return

    return google(match[0])
