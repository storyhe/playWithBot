#!/usr/bin/python
# -*- coding: utf8 -*-

"""!help ;지금 보고있는것."""

import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!help( .*)?", text)
    if not match: return

    helptopic = match[0].strip().encode("utf8")
    if helptopic:
        return server["hooks"]["help"].get(helptopic, "No help found for {0}".format(helptopic))
    else:
        return "\n".join(sorted(val for _, val in server["hooks"]["help"].iteritems()))
