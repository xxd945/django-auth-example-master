from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^base/', views.base, name='base'),
    url(r'^plot/(?P<place>[a-z]+)$', views.plot, name='plot'),
    url(r'^output/', views.output,name='output'),
    url(r'^test/', views.test,name='test'),
]
