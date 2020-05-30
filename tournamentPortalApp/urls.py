from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('tmp/', views.tmp, name='tmp'),
    path('tournaments/', views.tournamentList, name='tournamentList')
]