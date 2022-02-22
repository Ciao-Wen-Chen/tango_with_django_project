from django.urls import path 
from rango import views
from rango.models import UserProfile

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # indicate that we want to match a string which is a slug, 
    # and to assign it to variable category_name_slug
    path('category/<slug:category_name_slug>/',
        views.show_category, name='show_category'),
    
    # Chapter 7
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),

    #@ Chapter 8
    path('register/', views.register, name='register'),

    #@ Chapter 9
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]