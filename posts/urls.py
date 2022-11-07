from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:post_id>/<slug:post_slug>/',views.Postview.as_view(),name='post'),
    path('<int:post_id>/<slug:post_slug>/delete/',views.Postdelete.as_view(),name='post_delete'),
    path('<int:post_id>/<slug:post_slug>/update/',views.Postupdate.as_view(),name='post_update'),
    path('create/',views.Postcreate.as_view(),name='post_create'),
    path('reply/<int:post_id>/<int:comment_id>/',views.AddReplyview.as_view(),name='add_reply'),
    path('like/<int:post_id>/',views.PostLikeView.as_view(),name='like_post'),
    path('unlike/<int:post_id>/', views.PostUnlikeView.as_view(), name='unlike_post'),

]