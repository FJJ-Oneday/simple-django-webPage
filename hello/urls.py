from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from . import settings
from . import index
from web import views

urlpatterns = [
    path('', views.movie_list),
    path('web/', include('web.urls')),
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
