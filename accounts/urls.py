from re import template
from django.urls import path

from .views import ChangeUserInfoView, DeleteUserView, RegisterDoneView, RegisterUserView, ShortenerLoginView, ShortenerLogoutView, ShortenerPasswordChangeView, ShortenerProfile, RegisterUserView, RegisterDoneView, user_activate

app_name = 'auth'

urlpatterns = [
    path('password/change/', ShortenerPasswordChangeView.as_view(),
         name='password_change'),
    path('register/activate/<str:sign>/',
         user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('profile/', ShortenerProfile.as_view(), name='profile'),
    path('logout/', ShortenerLogoutView.as_view(), name='logout'),
    path('login/', ShortenerLoginView.as_view(), name='login'),
]
