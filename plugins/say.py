#!/usr/bin/python
# -*- coding: utf8 -*-

"""히든커멘드지롱"""

import re
from botlib import BotLib
from botlib._util import enum

Type = enum(
    Nico = 1,
    Kkamo = 2,
    Japan = 3,
    )

def input_to_type(text):
    if re.findall(ur"니코", text): return Type.Nico
    if re.findall(ur"까모", text): return Type.Kkamo
    if text == '!japan': return Type.Japan
    return None

#def get_argument(text):
#   return

def on_message(msg, server):
    text = msg.get("text", "")

    msgtype = input_to_type(text)

    if msgtype == Type.Nico:
        BotLib.say(msg['channel'], u"오타쿠 기분나빠...")
    if msgtype == Type.Kkamo:
        BotLib.say(msg['channel'], u"까모오......")
    if msgtype == Type.Japan:
        BotLib.say(msg['channel'], u"일본 또가?")
