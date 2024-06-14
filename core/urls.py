from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('forums/', views.forum, name="forums"),
    path('forums/<str:post_id>/', views.forum, name="forums"),
    path('midi_files/', views.midi_files, name="midi_files"),
    path('music_theory/', views.music_theory, name="music_theory"),
    path('profile/', views.profile, name="profile"),

    path('support/', views.support, name="support"),
    path('admin_support/', views.admin_support, name="admin_support"),
    path('admin_support/<str:user_id>/', views.admin_support, name="admin_support"),

]