from django.conf.urls import url

from . import views

app_name = 'listas'

urlpatterns = [
    url(r'^requerir/$', views.requerir_lista, name='requerir'),
    url(r'^criar/$', views.criar_lista, name='criar'),
]