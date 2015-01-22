#!/usr/bin/python
# -*- coding: utf-8 -*-

"""!무기정보 <무기명>; 무기의 정보를 봅니다."""

import botlib, json, re, random

def on_message(msg, server):
    text = msg.get("text", "")
    if text == u"!무기정보":
     return unicode("사용방법: !무기정보 <무기명> \n안내: 무기명에는 찾을 무기를 입력해주십시요.", "utf8")

    match = re.findall(u"!(?:무기정보) (.*)", text)
    if not match: return
    
    searchterm = match[0].encode("utf8")
    
    return botlib.infoweapon(searchterm)
