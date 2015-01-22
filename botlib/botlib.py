#!/usr/bin/python
# -*- coding: utf8 -*-

from pymongo import MongoClient
import random


def mongdb():
	client = MongoClient('localhost', 27017)
	db = client['slackbot']
	return db

def exists_userid(userid):	
	# 사용자 기본데이터 collection 은 users 입니다
	
	collection = mongdb()['users']
	if collection.find_one({"userid": userid}) is not None:
		return True
	else:
		return False
	
	
def useradd(userid, nickname):
	# 사용자 기본데이터 collection 은 users 입니다.
	collection = mongdb()['users']
	collection.insert({"userid": userid, "nickname": nickname, "level": 1, "point": 100000})
	return True
	
def getuserInfo(userid):
	collection = mongdb()['users']
	return collection.find_one({"userid": userid})
	
def Checkweapon(weaponName):
	collection = mongdb()['weapon']
	if collection.find_one({"name": weaponName}) is not None:
		return True
	else:
		return False

def infoweapon(weaponName):
        collection = mongdb()['weapon']
        if collection.find_one({"name": weaponName}) is not None:
		data = collection.find_one({"name": weaponName})
                return unicode("무기명: %s / 파워 : %d", "utf8") % (data["name"], data["power"])
        else:
                return unicode("해당 무기는 없습니다.", "utf8")

def addweapon(weaponName):
	collection = mongdb()['weapon']
	power = random.randint(1, random.randint(10, 100))
	collection.insert({"name": weaponName, "power": power})
	return unicode("무기가 추가되었습니다. \n\n무기명: %s\n파워: %d", "utf8") % (weaponName, power)
