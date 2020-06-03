from django.urls import path

from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.index, name='index'),
    # path('tmp/', views.tmp, name='tmp'),
    path('tournaments/', views.TournamentList.as_view(), name='tournamentList'),
    path('tournaments/create', views.tournamentCreate, name='tournamentCreate'),
    path('tournaments/<int:pk>', views.TournamentDetail.as_view(), name='tournamentDetail')
]