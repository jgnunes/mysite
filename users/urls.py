from django.conf.urls import url, include

app_name = 'users'

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]