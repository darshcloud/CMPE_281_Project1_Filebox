from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path(r'^update/(?P<file_name>\w+/(?P<file_desc>\w+/(?P<uploaded_time>\w+/(?P<updated_time>\w+/$',
         views.update, name='update'),
    path(r'^delete/(?P<file_name>\w+/(?P<file_username>\w+/$', views.delete, name='delete'),
    path('logout/', views.logout_user, name='logout')
]
