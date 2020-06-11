from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('tmp/', views.tmp, name='tmp'),
    path('tournaments/', views.TournamentList.as_view(), name='tournamentList'),
    path('tournaments/create', views.tournamentCreate, name='tournamentCreate'),
    path('tournaments/create/request', views.tournamentCreateRequest, name='tournamentCreateRequest'),
    path('tournaments/<int:pk>', views.TournamentDetail.as_view(), name='tournamentDetail'),
    path('tournaments/<int:tournament_id>/sponsors/create', views.sponsorCreate, name='sponsorCreate'),
    path('tournaments/<int:tournament_id>/sponsors/create/request', views.sponsorCreateRequest, name='sponsorCreateRequest'),
    path('users/login/', views.userLogin, name="userLogin"),
    path('users/login/request', views.userLoginRequest, name="userLoginRequest"),
    path('users/logout', views.userLogout, name="userLogout"),
    path('users/register', views.portalUserRegister.as_view(), name="userRegister"),
    path('users/activate/<str:uuid_base64>/<str:token>', views.portalUserActivate, name="userRegisterActivate")
]