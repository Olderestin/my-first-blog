from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', cache_page(60*60*24)(views.post_new), name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('search/', views.Search.as_view(), name='search'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete')
]
