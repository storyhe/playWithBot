#!/usr/bin/python
# -*- coding: utf8 -*-

"""!say <문장>; 이걸 따라합니다."""

import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:say) (.*)", text)
    if not match: return

    return match[0]

