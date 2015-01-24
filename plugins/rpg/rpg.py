#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import json
import math

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
        if not self.__check_weapon(weaponname) :
            return u"해당 무기는 없습니다."
        (name, level, power) = self.__get_weapon_info(weaponname)
        return u"무기명: %s[lv.%d] / 파워 : %d" % (name, level, power)


    def add_weapon(self, userobj, weaponname) :
        if self.__check_weapon(weaponname) :
            return u"이미 해당 무기가 등록되어있습니다."
        else:
            return self.__add_weapon(weaponname) + self.get_weapon_info(userobj, weaponname)

    def upgrade_weapon(self, userobj, weaponname) :
        if not self.__check_weapon(weaponname) :
            return u"해당 무기는 없습니다."
        (name, level, power) = self.__get_weapon_info(weaponname)
        possibility = self.__weapon_upgrade_possibility(level)
        text = u"무기를 업그레이드 합니다 (성공확률:%5.2f%%)..................."%(possibility*100)
        if possibility > random.random():
            text += u"성공!\n"
            text += u"무기강화에 성공하였습니다. \n"
            text += self.__upgrade_weapon(weaponname)
        else:
            # 레벨이 높을수록 대실패할 확률이 높아짐
            if random.randint(1, 100/level) == 1:
                text += u"대실패.......\n"
                text += u"처참하게 실패하였습니다. \n"
                text += self.__downgrade_weapon(weaponname, True)
            else:
                text += u"실패....\n"
                text += u"무기강화에 실패하였습니다. \n"
                text += self.__downgrade_weapon(weaponname, False)
            
        text += self.get_weapon_info(userobj, weaponname)
        return text
        



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
        if not self.__check_weapon(weaponName):
            return
        collection = self.db['weapon']
        data = collection.find_one({"name": weaponName})
        return (data["name"], data["level"], data["power"])
    
    def __add_weapon(self, weaponName):
        collection = self.db['weapon']
        power = random.randint(1, random.randint(10, 100))
        collection.insert({"name": weaponName, "power": power, "level": 1})
        return u"무기가 추가되었습니다. \n"

    def __upgrade_weapon(self, weaponName):
        collection = self.db['weapon']
        data = collection.find_one({"name": weaponName})
        (power, level) = (data["power"], data["level"])
        collection.update({"name": weaponName}, {"$set": {"power": math.floor(power*1.05), "level": level+1}})
        text = u"%s의 공격력이 %d만큼 증가했습니다.\n" % (weaponName, math.floor(power*1.05) - power)
        return text

    def __downgrade_weapon(self, weaponName, bigfail):
        collection = self.db['weapon']
        data = collection.find_one({"name": weaponName})
        (power, level) = (data["power"], data["level"])
        text = ''
        if bigfail:
            collection.update({"name": weaponName}, {"$set": {"power": math.floor(power/math.pow(1.05,level-1)), "level": 1}})
            text = u"%s의 레벨이 1로 떨어졌습니다.\n" % weaponName
        else:
            collection.update({"name": weaponName}, {"$set": {"power": math.floor(power/1.05), "level": level-1}})
            text = u"%s의 공격력이 %d만큼 감소했습니다.\n" % (weaponName, math.floor(power/1.05) - power)
        return text

    @staticmethod
    def __weapon_upgrade_possibility(level):
        return math.exp(-((level-2.0)/8))