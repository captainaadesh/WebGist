import requests

from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)


@main.route('/')
def index():
	search_url = 'https://www.googleapis.com/youtube/v3/search'

	search_params = {
		'key' : current_app.config['YOUTUBE_API_KEY'],
		'q' : 'flask',
		'part': 'snippet',
		'maxResults' : 3,
		'type': 'video' 
	}

	r = requests.get(search_url, params=search_params)

	print(r.json()['items'][0]['id']['videoId']) 

	return render_template('index.html')