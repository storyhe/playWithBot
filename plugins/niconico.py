#!/usr/bin/python
# -*- coding: utf8 -*-

"""니코 니코니코니"""

from urllib import quote
import re
import requests
from random import shuffle


def on_message(msg, server):
	text = msg.get("text", "").encode("utf8")

	if (text == "니코"):
		return u"니코니코니~"

