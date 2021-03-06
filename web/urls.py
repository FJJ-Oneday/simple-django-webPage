from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    path('send-mail/', views.send_email, name='send_mail'),
    path('login/', views.login, name='login'),
    path('is_login/', views.is_login, name='is_login'),
    path('admin/', views.admin, name='admin'),
    path('spider/', views.spider, name='spider'),
    path('movie-pic/', views.movie_list, name='movie-pic'),
    path('register/', views.register, name='register'),
    path('register-page/', views.register_page, name='register-page'),
]