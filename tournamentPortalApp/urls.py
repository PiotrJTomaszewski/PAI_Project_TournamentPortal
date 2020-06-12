from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('tmp/', views.tmp, name='tmp'),
    path('tournaments/', views.TournamentList.as_view(), name='tournamentList'),
    path('tournaments/create', views.TournamentCreate.as_view(), name='tournamentCreate'),
    path('tournaments/<uuid:pk>', views.TournamentDetail.as_view(), name='tournamentDetail'),
    path('tournaments/<uuid:pk>/sponsors/create', views.SponsorCreate.as_view(), name='sponsorCreate'),
    path('users/login/', views.PortalUserLogin.as_view(), name="userLogin"),
    path('users/logout', views.portalUserLogout, name="userLogout"),
    path('users/dashboard/<uuid:pk>', views.portalUserDashboard.as_view(), name="userDashboard"),
    path('users/register', views.portalUserRegister.as_view(), name="userRegister"),
    path('users/activate/<str:uuid_base64>/<str:token>', views.PortalUserActivate, name="userRegisterActivate"),
    path('users/password/forgot', views.PortalUserPasswordForgotten.as_view(), name="userPasswordForgotten"),
    path('users/<str:uuid_base64>/password/reset/<str:token>', views.portalUserResetPassword, name="userPasswordReset")
]