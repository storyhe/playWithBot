#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import json

class RPG:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        
################################### public  ####################################

    def add_user(self, userobj):
        if not userobj["ok"]:
            return u"서버와 연동에 실패하였습니다."

        userNickname = userobj["user"]["profile"]["real_name"]
        userId = userobj['user']['id']

        text = ""
        
        if (self.__exists_userid(userId) == False):
            text = u"환영합니다! 본격 잉여ゲーム 참여주셔서 감사합니다. %s 님" % userNickname
            if (self.__add_user(userId, userNickname) == True):
                text += u"\n\n감사합니다. DB에 정상적으로 등록되었습니다. \n *닉네임은 변경하셔도 지금 닉네임으로 저장되오니 갱신 명령어로 갱신하시길 바랍니다.\n\n 내정보는 !내정보 , !도움 을 말씀하시면 명령어를 보실수 있습니다."
            else:
                text += u"서버등록에 실패하였습니다. 관리자에게 문의 하시길 바랍니다."
        else:
            text = u"이미 가입되어있습니다"
        return text
        
        
    def get_user_info(self, userobj):
        userId = userobj['user']['id']
        if (self.__exists_userid(userId) == False):
            return u"미가입대상자입니다. 가입부터 진행해주세요"
        else:
            data = self.__get_user_info(userId)
            return u"> *%s* [Lv:%d / 포인트: %d]" % (data["nickname"], data["level"], data["point"])


    def get_weapon_info(self, userobj, weaponname) :
        return self.__get_weapon_info(weaponname)


    def add_weapon(self, userobj, weaponname) :
        if self.__check_weapon(weaponname) :
            return u"이미 해당 무기가 등록되어있습니다."
        else:
            return self.__add_weapon(weaponname)



################################### private ####################################
        
    def __exists_userid(self, userid):    
        # 사용자 기본데이터 collection 은 users 입니다
        
        collection = self.db['users']
        if collection.find_one({"userid": userid}) is not None:
            return True
        else:
            return False
        
    def __add_user(self, userid, nickname):
        # 사용자 기본데이터 collection 은 users 입니다.
        collection = self.db['users']
        collection.insert({"userid": userid, "nickname": nickname, "level": 1, "point": 100000})
        return True
        
    def __get_user_info(self, userid):
        collection = self.db['users']
        return collection.find_one({"userid": userid})
        
    def __check_weapon(self, weaponName):
        collection = self.db['weapon']
        if collection.find_one({"name": weaponName}) is not None:
            return True
        else:
            return False
    
    def __get_weapon_info(self, weaponName):
            collection = self.db['weapon']
            if collection.find_one({"name": weaponName}) is not None:
                data = collection.find_one({"name": weaponName})
                return u"무기명: %s / 파워 : %d" % (data["name"], data["power"])
            else:
                return u"해당 무기는 없습니다."
    
    def __add_weapon(self, weaponName):
        collection = self.db['weapon']
        power = random.randint(1, random.randint(10, 100))
        collection.insert({"name": weaponName, "power": power})
        return u"무기가 추가되었습니다. \n\n무기명: %s\n파워: %d" % (weaponName, power)

