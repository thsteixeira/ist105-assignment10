from django.urls import path

from . import views

urlpatterns = [
    path('', views.continent_view, name='continent_view'),
    path('history/', views.history_view, name='history_view'),
]
