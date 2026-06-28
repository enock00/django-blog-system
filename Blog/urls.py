from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:id>/', views.post_update, name='post_update'),
    path('delete/<int:id>/', views.delete_post, name='post_delete'),
    path('register/', views.register, name='register'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('profile/', views.profile, name='profile'),
    path('my_posts/', views.my_posts, name='my_posts'),
]
