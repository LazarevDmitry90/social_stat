import json
import time
from datetime import datetime

from flask import Flask, abort, request, jsonify, render_template 
import requests

import config
from vk_data import get_wall_group_stat, get_common_group_stat, prepare_group_stat, prepare_common_group_stat, get_group_info, \
get_group_ids_list


APP = Flask(__name__)

@APP.route("/")
def index():
	group_list_raw = get_group_info(config.GROUP_API_ENDPOINT)
	group_list_dict= get_group_ids_list(group_list_raw)
	group_list = list(group_list_dict.keys())
	print(type(group_list_dict))

	if request.args.get('group_id'):
		config.GROUP_ID = '-' + request.args.get('group_id')

	current_group_name = group_list_dict[int(config.GROUP_ID[1:])]

	raw_group_stat = get_wall_group_stat(config.WALL_API_ENDPOINT)
	raw_common_group_stat = get_common_group_stat(config.GROUP_STAT_API_ENDPOINT)
	likes_stat, likes_table, xaxis_likes, reposts_stat = prepare_group_stat(raw_group_stat)
	views_stat, xaxis_views = prepare_common_group_stat(raw_common_group_stat)
	return render_template(
		'index.html',
		likes_stat=likes_stat,
		likes_table=likes_table,
		xaxis_likes=xaxis_likes,
		reposts_stat=reposts_stat,
		views_stat=views_stat,
		xaxis_views=xaxis_views,
		group_list=group_list,
		current_group_name=current_group_name,
		group_list_dict=group_list_dict,
		)


if __name__ == "__main__":
	APP.run(port=1234, debug=True)


