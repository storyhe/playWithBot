#!/usr/bin/python
# -*- coding: utf-8 -*-

"""!whoami """

from urllib import quote
import re, json
import requests
from random import shuffle


def on_message(msg, server):
	text = msg.get("text", "")
	if (text == "!whoami"):
		unix_userId = msg["user"]
		object = json.loads(server['client'].server.api_call("users.info", user = str(unix_userId)))
		if str(object["ok"] == "true"):
			profile = object["user"]["profile"]
			userNickname = profile["real_name"]
			text = unicode("안녕하세요! %s 님","utf-8") % userNickname
			return text
		else:
			return u"서버와 연동에 실패하였습니다."

