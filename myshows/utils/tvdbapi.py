import requests,json,os,time
from django.conf import settings
from datetime import datetime
from urllib import quote

def get_new_token():

	username='cadet'
	apikey='88A9CA054E15EC2D'
	userkey='1B2B1184D7439647'
	data=json.dumps({'apikey':apikey,'username':username,'userkey':userkey})
	url="https://api.thetvdb.com/login"
	headers={'Content-type':'application/json','Accept':'application/json','User-Agent':'Mozilla/5.0'}
	r=requests.post(url,data=data,headers=headers)
	return r.json()['token']

def get_token():

	modify_time = os.path.getmtime(os.path.join(settings.PROJECT_ROOT, 'token.datas'))
	if time.time() - modify_time > 82800:
		try :
			new_token = get_new_token()
		except:
			print('API MUST BE DOWN')
		with open(os.path.join(settings.PROJECT_ROOT, 'token.datas'),'w') as file:
			file.write(new_token)
	with open(os.path.join(settings.PROJECT_ROOT, 'token.datas')) as file:
		token = file.read()
	return (token)

def search_series_list(series_name):

	token=get_token()
	headers={'Content-type':'application/json','Accept':'application/json','Authorization':'Bearer '+token,'User-Agent':'Mozilla/5.0'}
	url='https://api.thetvdb.com/search/series?name='+quote(series_name)
	try:
		data=requests.get(url,headers=headers).json()
		return data['data'][:5]
	except:
		return None

def get_series_with_id(tvdbID):
	token = get_token()
	headers={"Content-Type":"application/json","Accept": "application/json",'Authorization' : 'Bearer '+token, "User-agent": "Mozilla/5.0"}
	url = 'https://api.thetvdb.com/series/' + str(tvdbID)
	try:
		json_r = requests.get(url, headers=headers).json()
		json_r = json_r['data']
		show_info = {}
		show_info['tvdbID'] = tvdbID
		show_info['seriesName'] = json_r['seriesName']
		show_info['banner'] = json_r['banner']
		show_info['status'] = json_r['status']
		show_info['firstAired'] = json_r['firstAired']
		show_info['overview'] = json_r['overview']
		show_info['imdbID'] = json_r['imdbId']
		show_info['genre'] = json_r['genre']
		show_info['siteRating'] = json_r['siteRating']
		show_info['network'] = json_r['network']
		return show_info
	except:
		return None

def get_season_episode_list(tvdbID, number):
	token = get_token()
	headers={"Content-Type":"application/json","Accept": "application/json",'Authorization' : 'Bearer '+token, "User-agent": "Mozilla/5.0"}
	url = 'https://api.thetvdb.com/series/' + str(tvdbID) + '/episodes/query?airedSeason=' + str(number)
	try:
		json_r = requests.get(url, headers=headers).json()
		season_data = []
		json_r = json_r['data']
		for episode in json_r:
			episode_data = {}
			episode_data['number'] = episode['airedEpisodeNumber']
			episode_data['episodeName'] = episode['episodeName']
			episode_data['firstAired'] = episode['firstAired']
			episode_data['tvdbID'] = episode['id']
			episode_data['overview'] = episode['overview']
			season_data.append(episode_data)
		return season_data
	except:
		return None

def get_all_episodes(tvdbID,start_season):
	show = {}
	for i in range(start_season,100):
		season_data = get_season_episode_list(tvdbID, i)
		if season_data:
			show['Season'+str(i)] = season_data
		else:
			break
	return show

	

