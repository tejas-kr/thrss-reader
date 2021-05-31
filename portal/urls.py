
from django.urls import path

from . import views
from . import views_index

urlpatterns = [
    path('', views_index.index, name='index'),
    path('news/<str:type>/', views.news, name = 'news'),
    path('nlp/<str:type>/', views.nlp, name='nlp'),
]
