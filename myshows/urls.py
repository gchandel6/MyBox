from django.conf.urls import url

from .views import ( home , add_search , add , single_show , delete_show , update_rating , episode_change_status , season_change_status , update_show_data
	, recommended)

urlpatterns = [
	
	url(r'^(?P<view_type>|all||)$',home ),
	url(r'^add_search',add_search),
	url(r'^add',add),
	url(r'^show/(?P<show_slug>[a-zA-Z0-9-]*$)', single_show),
	url(r'^delete_show',delete_show),
	url(r'^update_rating',update_rating),
	url(r'^episode_change_status',episode_change_status),
	url(r'^season_change_status',season_change_status),
	url(r'^update_show_data',update_show_data),
	url(r'^recommendations',recommended)
]


