# 1) отдельный скрипт на Flask, который из указанной группы в ВК достает статистику по группе
# в гете передается ID группы, на выходе статистика группы по лайкам и репостам

# 2) сделать вывод данных в таблице на странице фронта плюс-минус красиво




# защищенный ключ
# AxD7aQlBdpfUCAxexDaG


# сервисный ключ доступа
# 108119361081193610db837fc910da3877110811081193648696ce13343d9fd49bf0bc8


# получение авторизации
# https://oauth.vk.com/authorize?client_id=5972289&redirect_uri=vk.com&scope=notify,friends,wall,offline,groups,stats&display=page&response_type=token&state=zalupa

# токен
# http://api.vk.com/blank.html#access_token=283c430895f6d738928e3933b282154c28e0c40647116f647a216778db02e187c5e0c4e40c08a5b6b877a&expires_in=0&user_id=1626924&state=zalupa

# получение групп, где пользователь админ
# https://api.vk.com/method/groups.get?extended=1&user_id=1626924&count=7&v=5.63&access_token=283c430895f6d738928e3933b282154c28e0c40647116f647a216778db02e187c5e0c4e40c08a5b6b877a&user_id=1626924

# статистика по постам группы
# https://api.vk.com/method/wall.get?owner_id=-412597&user_id=1626924&v=5.63&access_token=283c430895f6d738928e3933b282154c28e0c40647116f647a216778db02e187c5e0c4e40c08a5b6b877a&app_id=5972289&count=100


from flask import Flask, abort, request, jsonify

import requests

import json

import time

from datetime import datetime


user_id='1626924' #мой пользователь
access_token='283c430895f6d738928e3933b282154c28e0c40647116f647a216778db02e187c5e0c4e40c08a5b6b877a' #токен для моего пользователя
app_id='5972289' #мое приложение learn_python в ВК
oduvan_group='-412597' #группа в ВК ФК ОдуванчЭк, где я админ
v_api='5.63' #последняя версия API VK
wall_api='https://api.vk.com/method/wall.get?count=100'

app = Flask(__name__)



@app.route("/")
def index():
	def get_wall_group_stat(url):
		result = requests.get(url)
		if result.status_code == 200:
			return result.json()
		else:
			print("что-то пошло не так")

	url = "%s&owner_id=%s&user_id=%s&v=%s&access_token=%s&app_id=%s" % (wall_api, oduvan_group, user_id, v_api, access_token, app_id)
	oduvan_stat = get_wall_group_stat(url)
	to_paste = ''

	raw_post_info = oduvan_stat['response']['items']
	print(type(oduvan_stat['response']['items']))

	likes_stat = {
		# 201602: 2
	}

	for raw_stat_item in raw_post_info:
		if likes_stat.get('date') == time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date'])):
			likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = int(likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))]) + int(raw_stat_item['likes']['count'])
		else:
			likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = raw_stat_item['likes']['count']

	print(likes_stat['2013-10-14'])


	for date, likes_amount in sorted(likes_stat.items(),reverse=True):

		to_paste += '<tr><td>%s</td><td><center>%s</center></td></tr>' % (
			date,
			likes_amount,
		)
	print(to_paste)



	return '''
<table>
	<tr>
		<th>Дата</th>
		<th>Количество лайков</th>
	</tr>
	<tr>%s</tr>
</table>''' % to_paste




if __name__ == "__main__":
	app.run(port=1234, debug=True)


