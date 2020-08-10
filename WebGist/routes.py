import requests

from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
	search_url = 'https://www.googleapis.com/youtube/v3/search'
	video_url = 'https://www.googleapis.com/youtube/v3/videos'

	videos = []

	if request.method == 'POST':

		search_params = {
			'key' : current_app.config['YOUTUBE_API_KEY'],
			'q' : request.form.get('searchgist'),
			'part': 'snippet',
			'maxResults' : 6,
			'type': 'video'
		}

		r = requests.get(search_url, params=search_params)

		results = r.json()['items']

		gists = []

		for i in results:
			gists.append(i['id']['videoId'])


		video_params = {
			'key' : current_app.config['YOUTUBE_API_KEY'],
			'id' : ','.join(gists),
			'part' : 'snippet, contentDetails',
			'maxResults' : 6
		}
		
		r = requests.get(video_url, params=video_params)

		results = r.json()['items']


		for i in results:

			gist_data = {
				'id' : i['id'],
				'url' : f'https://www.youtube.com/watch?v={ i["id"] }',
				'thumbnail' : i['snippet']['thumbnails']['high']['url'],
				'duration' : int(parse_duration(i['contentDetails']['duration']).total_seconds()// 60),
				'title' : i['snippet']['title'],
			}
			videos.append(gist_data)

	return render_template('index.html', videos=videos)