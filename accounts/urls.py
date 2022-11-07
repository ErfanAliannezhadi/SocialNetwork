from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.Registerview.as_view(), name='user_register'),
    path('login/', views.Loginview.as_view(), name='user_login'),
    path('logout/', views.Logoutview.as_view(), name='user_logout'),
    path('profile/<user_id>/<user_name>/', views.Profileview.as_view(), name='user_profile'),
    path('resetpassword/', views.Userpasswordresetview.as_view(), name='reset_password'),
    path('resetpassword/done/', views.Userpasswordresetdoneview.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.Userpasswordresetconfirmview.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.Userpasswordresetcompleteview.as_view(), name='password_reset_complete'),
    path('follow/<user_id>/', views.Userfollowview.as_view(), name='user_follow'),
    path('unfollow/<user_id>/', views.Userunfollowview.as_view(), name='user_unfollow'),
    path('editprofile', views.EditProfileView.as_view(), name='edit_profile'),

]