import json
import time
from datetime import datetime
from itertools import groupby

import requests

import config

def get_group_info(url, extra_params=None):
	params = {
	'count': 1000,
	'user_id': config.USER_ID,
	'v': config.V_API,
	'access_token': config.ACCESS_TOKEN,
	'extended': 1,
	'filter': 'admin',
	}
	if extra_params:
		params.update(extra_params)

	result = requests.get(url, params=params)
	if result.status_code == 200:
		return result.json()
	else:
		print("что-то пошло не так")


def get_group_ids_list(raw_data):
	print(raw_data)
	new_raw_data=raw_data['response']['items']
	# group_list=[]
	# for item in new_raw_data:
	# 	group_list.append(item['id'])

	group_list_dict={
	# group_id: group_name
	}
	for item in new_raw_data:
		group_list_dict[item['id']] = item['name']

	return group_list_dict



def get_wall_group_stat(url, extra_params=None):
	params = {
		'count': 100,
		'owner_id': config.GROUP_ID,
		'user_id': config.USER_ID,
		'v': config.V_API,
		'access_token': config.ACCESS_TOKEN,
		'app_id': config.APP_ID,
	}
	if extra_params:
		params.update(extra_params)

	result = requests.get(url, params=params)
	if result.status_code == 200:
		return result.json()
	else:
		print("что-то пошло не так")


def get_common_group_stat(url, extra_params=None):
	params = {
		'group_id': config.GROUP_ID[1:],
		'user_id': config.USER_ID,
		'v': config.V_API,
		'access_token': config.ACCESS_TOKEN,
		'app_id': config.APP_ID,
		'date_from': config.DATE_FROM,
		'date_to': config.DATE_TO,
	}
	if extra_params:
		params.update(extra_params)

	result = requests.get(url, params=params)
	if result.status_code == 200:
		return result.json()
	else:
		print("что-то пошло не так")


def get_grouped_likes_stat(raw_data):
	likes_stat = {
		# 201602: 2
	}

	for raw_stat_item in raw_data:
		if raw_stat_item['post_type'] != 'suggest':
			if likes_stat.get('date') == time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date'])):
				likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = \
				int(likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))]) + int(raw_stat_item['likes']['count'])
			else:
				likes_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = raw_stat_item['likes']['count']

	likes_stat_new = sorted(list(likes_stat.items()))

	return likes_stat, likes_stat_new


def make_likes_table(grouped_likes_stat):
	likes_table = ''
	likes_stat = grouped_likes_stat
	for date, likes_amount in sorted(likes_stat.items(),reverse=True):
	# for date, likes_amount in likes_stat:
		likes_table += '<tr><td>%s</td><td><center>%s</center></td></tr>' % (
			date,
			likes_amount,
		)
	return likes_table


def get_grouped_reposts_stat(raw_data):
	reposts_stat = {
	# 2016-02-01: 2
	}

	for raw_stat_item in raw_data:
		if raw_stat_item['post_type'] != 'suggest':
			if reposts_stat.get('date') == time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date'])):
				reposts_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = \
				int(reposts_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))]) + int(raw_stat_item['reposts']['count'])
			else:
				reposts_stat[time.strftime("%Y-%m-%d", time.localtime(raw_stat_item['date']))] = raw_stat_item['reposts']['count']

	reposts_stat_new = sorted(list(reposts_stat.items()))

	return reposts_stat_new


def prepare_group_stat(raw_data):
	group_stat = raw_data

	raw_post_info = group_stat['response']['items']

	likes_stat_dict, likes_stat = get_grouped_likes_stat(raw_post_info)

	likes_table = make_likes_table(likes_stat_dict)

	reposts_stat = get_grouped_reposts_stat(raw_post_info)

	x_axis = sorted(list(likes_stat_dict.keys()))

	return likes_stat, likes_table, x_axis, reposts_stat


def prepare_common_group_stat(raw_data):
	common_group_stat = raw_data
	raw_group_stat_info = common_group_stat['response']

	views_stat = {
	# 2016-02-01: 2
	}

	for raw_stat_item in raw_group_stat_info:
			views_stat[raw_stat_item['day']] = raw_stat_item['views']

	views_stat_new = sorted(list(views_stat.items()))
	xaxis_views = sorted(list(views_stat.keys()))

	return views_stat_new, xaxis_views









