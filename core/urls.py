from django.contrib import admin
from django.urls import path

from frontend.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:title>/', IndexView.as_view(), name='index'),
]
