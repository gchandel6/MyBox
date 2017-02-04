from myshows.models import Show
import pandas as pd
import os

cols = [
'SeriesName',
'tvdbID',
'Network',
'tvdbRating',
'indicator']

genres = [
'Action',
'Adventure',
'Animation',
'Children',
'Comedy',
'Crime',
'Documentary',
'Drama',
'Family',
'Fantasy',
'Food',
'Game Show',
'Home and Garden',
'Horror',
'Mini-Series',
'Mystery',
'News',
'Reality',
'Romance',
'Science-Fiction',
'Soap',
'Special Interest',
'Sport',
'Suspense',
'Talk Show',
'Thriller',
'Travel',
'Western',
]
module_dir = os.path.dirname(__file__)

def build_training_set():
	tv_df = pd.DataFrame(columns=cols+genres)
	try:
		show_data = Show.objects.all()
		for show in show_data:
			show_genre_list = [0]*28
			show_genre = show.get_genres
			length = len(show_genre)
			for genre in show_genre:
				show_genre_list[genres.index(genre)] = (1.0/length)
			show_datas = [show.series_name, show.tvdbID , show.network, int(show.userRating), (float(show.siteRating)**2)*float(show.userRating)]
			tv_df = tv_df.append(pd.DataFrame([show_datas+show_genre_list], columns=cols+genres))
		
		tv_df.to_csv("myshows/utils/my_data.csv",encoding="utf-8")
		
		extended_tv_df=pd.read_csv('myshows/utils/my_data.csv')
		
		return extended_tv_df
	except:
		return tv_df
