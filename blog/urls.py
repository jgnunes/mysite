from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^index/$', views.posts_index, name='posts_index'),
    url(r'^index/show/$', views.posts_show, name='posts_show'),
]