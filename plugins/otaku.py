#!/usr/bin/python
# -*- coding: utf8 -*-

"""히든커멘드지롱"""

from urllib import quote
import re
import requests
from random import shuffle

def on_message(msg, server):
	text = msg.get("text", "")

	if (text == u"오타쿠"):
		return u"오타쿠 기분나빠"

