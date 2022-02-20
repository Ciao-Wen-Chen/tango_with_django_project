from django.urls import path 
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # indicate that we want to match a string which is a slug, 
    # and to assign it to variable category_name_slug
    path('category/<slug:category_name_slug>/',
        views.show_category, name='show_category')
]