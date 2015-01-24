#!/usr/bin/python
# -*- coding: utf-8 -*-

"""!가입; 봇 게임센터에 가입합니다.\n!내정보; 내 등록된 정보를 봅니다."""

import re
import json
from botlib import BotLib
from rpg import RPG
from util.util import enum

CmdType = enum(
    Register = 1,
    MyInfo = 2,
    WeaponInfo = 3,
    AddWeapon = 4,
    UpgradeWeapon = 5,
    )

# 입력으로부터 명령어 타입을 얻어내는 함수
def input_to_CmdType(text):
    if u"^!가입" == text: return CmdType.Register
    if u"^!내정보" == text: return CmdType.MyInfo
    if re.findall(u"^!무기정보 ", text): return CmdType.WeaponInfo
    if re.findall(u"^!무기추가 ", text): return CmdType.AddWeapon
    if re.findall(u"^!무기강화 ", text): return CmdType.UpgradeWeapon
    return None

# 입력으로부터 인자를 가져오는 함수
# 일단은 모든 인자가 오직 한개뿐이라 가정하고 만들었다....
# 인자가 없을 때 예외처리는 on_message()에서 try-except에서 처리
def get_argument(cmdType, text):
    match = None
    if cmdType == CmdType.WeaponInfo :
        match = re.findall(ur"^!무기정보 (.*)", text)
        if not match: raise ValueError
    if cmdType == CmdType.AddWeapon : 
        match = re.findall(ur"^!무기추가 (.*)", text)
        if not match: raise ValueError
    if cmdType == CmdType.UpgradeWeapon : 
        match = re.findall(ur"^!무기강화 (.*)", text)
        if not match: raise ValueError
    return match[0]

# 메인 명령을 실행하는 함수
def run_command(cmdType, text, msgobj, serverobj):
    
    userId = msgobj['user']
    userobj = BotLib.get_user_json_obj(userId, serverobj)
    channel = msgobj['channel']
    Rpg = RPG(BotLib)


    result = ''
    if cmdType == CmdType.Register :
        result = Rpg.add_user(userobj)
    if cmdType == CmdType.MyInfo :
        result = Rpg.get_user_info(userobj)
    if cmdType == CmdType.WeaponInfo :
        weaponname = get_argument(cmdType, text)
        result = Rpg.get_weapon_info(userobj, weaponname)
    if cmdType == CmdType.AddWeapon :
        weaponname = get_argument(cmdType, text)
        result = Rpg.add_weapon(userobj, weaponname)
    if cmdType == CmdType.UpgradeWeapon :
        weaponname = get_argument(cmdType, text)
        result = Rpg.upgrade_weapon(userobj, weaponname)
        
    BotLib.say(channel, result)
    

################################################################################

# slask 껍데기 함수
# 문자열을 return하면 봇이 그 말을 한다
def on_message(msg, server):
    text = msg.get("text", "")

    cmdType = input_to_CmdType(text)
    if not cmdType:
        return

    try:
        run_command(cmdType, text, msg, server['client'].server)
    except ValueError:
        if cmdType == CmdType.WeaponInfo :
            return u"사용방법: !무기정보 <무기명> \n안내: 무기명에는 찾을 무기를 입력해주십시요."
        if cmdType == CmdType.AddWeapon :
            return u"사용방법: !무기추가 <무기명> \n안내: 무기명에는 추가할 무기를 입력해주십시요."
        if cmdType == CmdType.UpgradeWeapon :
            return u"사용방법: !무기강화 <무기명> \n안내: 무기명에는 강화할 무기를 입력해주십시요."
