#!/usr/bin/python
# -*- coding: utf8 -*-

from pymongo import MongoClient
import json

class _BotLib():
    
    def __init__(self):
        self.client = None
        client = MongoClient('localhost', 27017)
        self.db = client['slackbot']

    def set_slack_client(self, client):
        self.client = client
        
    def say(self, channel, text):
        self.client.rtm_send_message(channel, text)
    
    def get_user_json_obj(self, userId, server):
        return json.loads(server.api_call("users.info", user = str(userId)))


# Singleton
BotLib = _BotLib()
