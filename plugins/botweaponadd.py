#!/usr/bin/python
# -*- coding: utf-8 -*-

"""!무기추가 <무기명>; 데이터베이스에 무기를 추가합니다."""

import botlib, json, re, random

def on_message(msg, server):
    text = msg.get("text", "")
    if text == u"!무기추가":
     return unicode("사용방법: !무기추가 <무기명> \n안내: 무기명에는 추가할 무기를 입력해주십시요.", "utf8")

    match = re.findall(u"!(?:무기추가) (.*)", text)
    if not match: return
    
    searchterm = match[0].encode("utf8")
    
    if searchterm is not "":
     if botlib.Checkweapon(searchterm) == True:
      return unicode("이미 해당 무기가 등록되어있습니다.", "utf-8")
     else:
      return botlib.addweapon(unicode(searchterm, "utf8"))
