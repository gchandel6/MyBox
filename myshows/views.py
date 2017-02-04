from django.shortcuts import render
from .models import Show,Episode,Season
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .utils.tvdbapi import search_series_list , get_series_with_id , get_all_episodes
from .utils.recommender import get_recommendations

# Create your views here.

def home(request,view_type):
	if view_type=="all":
		show_data=Show.objects.all().order_by('-modified')	
		flag=False
	else:
		show_data=Show.objects.all().order_by('-modified')
		data=[show for show in show_data if not show.is_watched]	
		show_data=data
		flag=True

	return render(request,'myshows/home.html',{'show_data':show_data , 'flag':flag })

@csrf_protect
def add_search(request):

	context={}
	context['Flag']=False

	if request.method=="POST":
		search_string=request.POST.get("search_string")
		search_results=search_series_list(search_string)
		if search_results is not None:
			context['show_datalist']=search_results
			context['Flag']=True

	return render(request,"myshows/add_search.html",{"context":context})


@csrf_protect
def add(request):
	if request.method=="POST":
		slug=""
		tvdbID=request.POST.get("show_id")
		runningStatus=request.POST.get("runningStatus")

		try:
			show=Show.objects.get(id=tvdbID)
			show=show.slug
		except Show.DoesNotExist as e:
			show_data=get_series_with_id(int(tvdbID))
			if show_data is not None:
				show=Show()
				show.add_show(show_data,runningStatus)
				slug=show.slug
				seasons_data = get_all_episodes(int(tvdbID), 1)
				for i in range(len(seasons_data)):
					string = 'Season' + str(i+1)
					season_data = seasons_data[string]
					season = Season()
					season.add_season(show, i+1)
					season_episodes_data = seasons_data[string]
					for season_episode in season_episodes_data:
						if season_episode['episodeName']:
							episode = Episode()
							episode.add_episode(season, season_episode)
		return HttpResponseRedirect('/show/%s'%slug)
	return HttpResponseRedirect('/all')

@csrf_protect
def single_show(request,show_slug):
	show=Show.objects.get(slug__iexact=show_slug)
	next_episode=show.next_episode
	return render(request,"myshows/single.html",{"show":show,"next_episode":next_episode})


@csrf_protect
def update_show_data(request):
	if request.method=='POST':
		show_id=request.POST.get("show_info")
		show=Show.objects.get(id=show_id)

		if show:
			show.update_show_data()
			show.last_updated=timezone.now()
			show.save()
			return HttpResponseRedirect('/show/%s'%show.slug)

		return HttpResponseRedirect('/')


@csrf_protect
def delete_show(request):
	if request.method=='POST':
		show_id=request.POST.get("show_id")
		if show_id:
			try:
				show=Show.objects.get(id=show_id)
				show.delete()
				return HttpResponseRedirect('/')
			except:
				return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')


@csrf_protect
def update_rating(request):
	if request.method=="POST":
		show_id=request.POST.get("show_id")
		new_rating=request.POST.get("new_rating")
		if show_id:
			show=Show.objects.get(id=show_id)
			show.userRating=new_rating
			slug=show.slug
			show.save()
		return HttpResponseRedirect("show/%s"%slug)
	return HttpResponseRedirect("/")


@csrf_protect
def episode_change_status(request):
	if request.method=="POST":
		episode_id=request.POST.get("episode_id")
		episode=Episode.objects.get(id=episode_id)
		episode.episode_status_change()
		slug=episode.season.show.slug
		return HttpResponseRedirect("show/%s"%slug)
	return HttpResponseRedirect("/")


@csrf_protect
def season_change_status(request):
	if request.method=="POST":
		season_id=request.POST.get("season_id")
		season=Season.objects.get(id=season_id)
		season.season_change_status()
		slug=season.show.slug
		return HttpResponseRedirect("show/%s"%slug)
	return HttpResponseRedirect("/")


def recommended(request):
	try:
		results=get_recommendations()
	except:
		results=[]

	all_data=[]
	for r in results:
		show=get_series_with_id(r)
		all_data.append(show)
	
	return render(request,"myshows/recommend.html",{ 'all_data':all_data })




