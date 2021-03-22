from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite

AdminSite.site_title = 'News-Agency'
AdminSite.site_header = 'News-Agency'

admin.site.register(Message)
