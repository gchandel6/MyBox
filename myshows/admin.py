from django.contrib import admin
from .models import Show,Episode,Season

# Register your models here.

admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)
