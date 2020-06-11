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
    path('users/login/', views.PortalUserLogin.as_view(), name="userLogin"),
    path('users/logout', views.userLogout, name="userLogout"),
    path('users/register', views.portalUserRegister.as_view(), name="userRegister"),
    path('users/activate/<str:uuid_base64>/<str:token>', views.PortalUserActivate, name="userRegisterActivate"),
    path('users/password/forgot', views.PortalUserPasswordForgotten.as_view(), name="userPasswordForgotten"),
    path('users/<str:uuid_base64>/password/reset/<str:token>', views.portalUserResetPassword, name="userPasswordReset")
]