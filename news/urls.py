from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    # nav
    path('', views.landing, name='landing'),
    path('health/', views.healthcheck, name='healthcheck'),

    # user
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.updateProfile, name='updateProfile'),
    path('profile/updatePic/', views.updatePicture, name='updatePicture'),
    path('profile/deletePic/', views.deletePicture, name='deletePicture'),
    path('login/', views.logging, name='logging'),
    path('logout/', views.logging_out, name='loggingout'),
    path('signup/', views.signup, name='signup'),
    path('articles/', views.getArticles, name='articles'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('reactions/', views.reactions, name='reactions'),
    path('comment/', views.comment, name='comment'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/', views.deletecomment, name='deletecomment'),
    path('editcomment/', views.editcomment, name='editcomment')
]