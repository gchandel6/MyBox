from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q
import json
from .utils.tvdbapi import get_series_with_id,get_season_episode_list,get_all_episodes

# Create your models here.


class Show(models.Model):
	tvdbID=models.CharField(max_length=50)
	series_name=models.CharField(max_length=50)
	overview=models.TextField()
	banner=models.CharField(max_length=140,null=True,blank=True)
	imbdID=models.CharField(max_length=50,null=True,blank=True)
	status_watched=models.BooleanField(default=False)
	slug=models.SlugField(null=True,blank=True)
	running_status=models.CharField(max_length=100)
	first_aired=models.DateField(null=True,blank=False)
	modified=models.DateTimeField(null=True,blank=False,auto_now=True,auto_now_add=False)
	siteRating=models.DecimalField(max_digits=5,null=True,decimal_places=3,blank=True,default=0)
	userRating=models.DecimalField(max_digits=5,null=True,decimal_places=3,blank=True,default=0)
	network=models.CharField(max_length=50)
	genre_list=models.TextField(null=True,blank=True)
	last_updated=models.DateTimeField(null=True,blank=True)

	def add_show(self,data,runningstatus):
		self.series_name=data['seriesName']
		self.slug=slugify(self.series_name)
		self.overview=data['overview']
		self.network=data['network']
		self.siteRating=data['siteRating']
		self.runningstatus=runningstatus
		self.banner='http://thetvdb.com/banners/'+data['banner']
		self.tvdbID=data['tvdbID']
		self.imbdID=data['imdbID']
		self.genre_list=json.dumps(data['genre'])
		self.last_updated=timezone.now()
		try:
			self.firstAired = datetime.strptime(data['firstAired'], '%Y-%m-%d').date()
		except:
			pass
		self.save()


	def __str__(self):
		return self.series_name

	@property
	def is_watched(self):
		flag=True
		all_seasons=Season.objects.filter(show=self)
		for season in all_seasons:
			if season.status_watched_check is False and season.episode_count is not 0:
				flag=False
				break
		return flag
		
	@property
	def episode_watch_count(self):
		return Episode.objects.all(Q(season__show=self) , Q(status_watched=False)).count()

	@property
	def all_episodes(self):
		return Episode.objects.all(season__show=self).count()

	@property 
	def next_episode(self):
		return Episode.objects.filter(Q(season__show=self) , Q(status_watched=False)).first()

	@property 
	def get_genres(self):
		return json.loads(self.genre_list)

	def update_show_data(self):
		flag=False
		tvdbID=self.tvdbID
		last_season=self.season_set.all().last()
		last_episodes=last_season.episode_set.all()
		new_episodes=get_season_episode_list(tvdbID,last_season.number)
		cnt=0

		if new_episodes:
			for (old_episode,new_episode) in zip(last_episodes,new_episodes):
				old_episode.compare_or_update(new_episode)
				cnt=cnt+1
			if cnt<len(new_episodes):
				flag=True
				for new_episode in new_episodes[cnt:]:
					if new_episode['episodeName']=="":
						new_episode['episodeName']="TBA"
					e=Episode()
					e.add_episode(last_season,new_episode)

			new_range=last_season.number+1
			new_seasons=get_all_episodes(tvdbID,new_range)

			for i in range(len(new_seasons)):
				flag=True
				s="Season"+str(i)
				cur_season_episodes=new_seasons[s]
				season=Season()
				season.add_season(self,i+new_range)

				for episode in cur_season_episodes:
					if episode['episodeName']:
						e=Episode()
						e.add_episode(season,episode)
		return flag



class Season(models.Model):
	show=models.ForeignKey(Show,on_delete=models.CASCADE)
	number=models.IntegerField()
	status_watched=models.BooleanField(default=False)

	def __str__(self):
		try:
			showname=self.show.series_name
			s=showname + " S" + str(self.number)
		except:
			s=""
		return s

	def add_season(self,show,number):
		self.show=show
		self.number=number
		self.save()

	@property 
	def watch_count(self):
		return Episode.objects.filter(Q(season=self),Q(status_watched=True),Q(first_aired__lte=datetime.now())).count()

	@property 
	def episode_count(self):
		return Episode.objects.filter(Q(season=self),Q(first_aired__lte=datetime.now())).count()

	@property 
	def status_watched_check(self):
		self.status_watched=( self.watch_count==self.episode_count )
		self.save()
		return self.status_watched

	def season_change_status(self):
		self.status_watched=not(self.status_watched)
		self.save()
		show=self.show
		all_episodes=Episode.objects.filter(season=self)
		
		if self.status_watched==False:
			all_episodes.update(status_watched=False)
		else:
			all_episodes.update(status_watched=True)
		show.save()


class Episode(models.Model):
	season=models.ForeignKey(Season , on_delete=models.CASCADE)
	ep_name=models.CharField(max_length=50,blank=True,null=True)
	number=models.IntegerField()
	first_aired=models.DateField(null=True,blank=False)
	date_watched=models.DateField(null=True,blank=False,auto_now=True,auto_now_add=False)
	status_watched=models.BooleanField(default=False)
	overview=models.TextField(null=True,blank=True)
	tvdb_id=models.CharField(max_length=50)

	def __str__(self):
		showname=self.season.show.series_name
		seasonnumber=self.season.number
		s=showname+" S "+str(seasonnumber)+" E"+str(self.number)
		return s

	def add_episode(self,season,data):
		self.season=season
		self.ep_name=data['episodeName']
		self.number=int(data['number'])
		try:
			self.first_aired=datetime.strptime(data['firstAired'],'%Y-%m-%d').date()
		except:
			pass
		self.tvdb_id=data['tvdbID']
		try:
			self.overview=data['overview']
		except:
			pass
		self.save()

	def episode_status_change(self):
		self.status_watched=not(self.status_watched)
		self.save()
		season=self.season
		show=season.show

		if season.episode_count == season.watch_count:
			season.status_watched=True
			season.save()
		else:
			season.status_watched=False
			season.save()
		show.save() 	

	def compare_or_update(self,new_episode):
		if self.ep_name=="" and new_episode['episodeName']!="":
			self.episodeName=new_episode['episodeName']
		if self.overview==None:
			self.overview=new_episode['overview']
		self.save()	

	

