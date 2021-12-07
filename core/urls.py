from django.contrib import admin
from django.urls import path

from frontend.views import IndexView, ScreenshotView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:title>/', IndexView.as_view(), name='index'),
    path('screenshots/<str:image_name>/', ScreenshotView.as_view(), name='index'),
]
