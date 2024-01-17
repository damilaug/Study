from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('room/<str:pk>/', views.room, name="room"),
    path("login", views.loginPage, name="login"),
    path("logout", views.LogoutUser, name='logout'),
    path('register', views.registerPage, name="register"),
    path('services/<str:pk>/', views.services, name="services"),
    path("about_us/", views.about_us, name="about_us"),
    path('create_room/', views.createRoom, name="create_room"),
    path("update_room/<str:pk>/", views.updateRoom, name="update_room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

]
