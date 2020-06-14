from django.urls import path

from . import views

urlpatterns = [
    path('', views.TournamentList.as_view(), name='index'),
    path('tournaments/', views.TournamentList.as_view(), name='tournamentList'),
    path('tournaments/create', views.TournamentCreate.as_view(), name='tournamentCreate'),
    path('tournaments/<uuid:pk>/edit', views.TournamentEdit.as_view(), name='tournamentEdit'),
    path('tournaments/<uuid:pk>', views.TournamentDetail.as_view(), name='tournamentDetail'),
    path('tournaments/<uuid:pk>/matches/json', views.tournamentMatchesJson, name='tournamentMatchesJson'),
    path('tournaments/<uuid:pk>/sponsors/create', views.SponsorCreate.as_view(), name='sponsorCreate'),
    path('tournaments/<uuid:pk>/participate', views.ParticipantCreate.as_view(), name="participantCreate"),
    # path('tournaments/<uuid:tournament_pk>/matches/result/add', views.matchAddResult, name='matchAddResult'),
    path('users/login/', views.PortalUserLogin.as_view(), name="userLogin"),
    path('users/logout', views.portalUserLogout, name="userLogout"),
    path('users/dashboard/<uuid:pk>', views.PortalUserDashboard.as_view(), name="userDashboard"),
    path('users/register', views.PortalUserRegister.as_view(), name="userRegister"),
    path('users/activate/<str:uuid_base64>/<str:token>', views.portalUserActivate, name="userRegisterActivate"),
    path('users/password/forgot', views.PortalUserPasswordForgotten.as_view(), name="userPasswordForgotten"),
    path('users/<str:uuid_base64>/password/reset/<str:token>', views.portalUserResetPassword, name="userPasswordReset"),
    path('debug/forcepair/<uuid:uuid>', views.debugForcePairUp, name="forcePairUp")
]