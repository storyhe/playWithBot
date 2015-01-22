#!/usr/bin/python
# -*- coding: utf-8 -*-

"""!가입; 봇 게임센터에 가입합니다.\n!내정보; 내 등록된 정보를 봅니다."""

import botlib, json

def on_message(msg, server):
	text = msg.get("text", "")
	if (text == "^!whoami"):
		unix_userId = msg["user"]
		object = json.loads(server['client'].server.api_call("users.info", user = str(unix_userId)))
		if str(object["ok"] == "true"):
			profile = object["user"]["profile"]
			userNickname = profile["real_name"]
			text = unicode("안녕하세요! %s 님","utf-8") % userNickname
			return text
		else:
			return u"서버와 연동에 실패하였습니다."

	elif (text == u"^!가입"):
		unix_userId = msg["user"]
		object = json.loads(server['client'].server.api_call("users.info", user = str(unix_userId)))
		
		if str(object["ok"] == "true"):
			profile = object["user"]["profile"]
			userNickname = profile["real_name"]
			if (botlib.exists_userid(unix_userId) == False):
				text = unicode("환영합니다! 본격 잉여ゲーム 참여주셔서 감사합니다. %s 님","utf-8") % userNickname
				if (botlib.useradd(unix_userId, userNickname) == True):
					text = text + unicode("\n\n감사합니다. DB에 정상적으로 등록되었습니다. \n *닉네임은 변경하셔도 지금 닉네임으로 저장되오니 갱신 명령어로 갱신하시길 바랍니다.\n\n 내정보는 !내정보 , !도움 을 말씀하시면 명령어를 보실수 있습니다.", "utf-8")
				else:
					text = text + unicode("서버등록에 실패하였습니다. 관리자에게 문의 하시길 바랍니다.", "utf-8")
			else:
				text = unicode("이미 가입되어있습니다", "utf-8")
			
			return text
			
		else:
			return u"서버와 연동에 실패하였습니다."

	elif (text == u"^!내정보"):
		unique_userid = msg["user"]
		if (botlib.exists_userid(unique_userid) == False):
			return unicode("미가입대상자입니다. 가입부터 진행해주세요", "utf8")
		else:
			data = botlib.getuserInfo(unique_userid)
			return unicode("> %s [Lv:%d / 포인트: %d]", "utf8") % (data["nickname"], data["level"], data["point"])
			
	elif (text == u"^!빵꾸똥꾸"):
		unix_userId = msg["user"]
		return json.dumps(server['client'].server.api_call("channels.kick", channel = str(msg["channel"]), user = str(unix_userId)))
