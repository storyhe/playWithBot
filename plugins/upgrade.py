# -*- coding: utf8 -*-
"""!강화 <무기이름> : 강화를 시도하여 강화 결과를 알려줍니다. 강화 성공 확률은 50%입니다."""
import re
from urllib import quote
import requests
import random

def has_jongsung(text):
    c = text[-1]
    return len(re.findall(u'[가-힣]', c)) != 0 and (ord(c) - 44032) % 588 % 28
    
def s(text, suffix):
    result = u''
    if suffix == u'을' or suffix == u'를':
        result = u'을' if has_jongsung(text) else u'를'
    if suffix == u'이' or suffix == u'가':
        result = u'이' if has_jongsung(text) else u'가'
    if suffix == u'은' or suffix == u'는':
        result = u'은' if has_jongsung(text) else u'는'
    if suffix == u'이다' or suffix == u'다':
        result = u'이다' if has_jongsung(text) else u'다'
    result = u"[" + text + u"]" + result
    return result

def success_msg(name):
    return random.choice([
        s(name, u"는") + u" 휘황찬란하게 빛납니다....!!",
        s(name, u"가") + u" 크고 아름다워졌습니다.... 우홋.... 멋진 " + s(name,u"다") + u"...",
        s(name, u"는") + u" 강인해졌습니다.....!",
        s(name, u"는") + u" 단단해졌습니다.....!",
        s(name, u"는") + u" 날카로워졌습니다.....!",
        ])
    
def fail_msg(name):
    return random.choice([
        s(name, u"는") + u" 형체를 알수 없을정도로 비틀어졌습니다...",
        s(name, u"가") + u" 괴생물체로 변해서 도망가버렸습니다...",
        s(name, u"는") + u" 한줌의 먼지가 되어 사라져버렸습니다.....",
        s(name, u"는") + u" 이제 이 세상의 물건이 아니게 되어버렸습니다.....",
        s(name, u"는") + u" 구세계와 신세계 사이의 어딘가로 공간이동해버렸습니다.....",
        ])

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(u"!강화 (.*)", text)
    if not match: return 
    
    weaponName = match[0]
    
    if not weaponName : return u"뭘 강화할건지 알려주세요..."
    
    result = random.random() > 0.5
    
    msg = u''
    if result :
        msg = u"강화성공! " + success_msg(weaponName)
    else:
        msg = u"강화실패............. " + fail_msg(weaponName)
        

    return s(weaponName, u"을") + u' 강화합니다....................... ' + msg
