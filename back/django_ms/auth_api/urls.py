from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    re_path('logout', views.logout_view),
    re_path('get_search_id', views.get_search_id),
    path('setSearchFavorite/<int:id>/', views.update_search_is_favorite),
    path('updateSearchName/<int:id>/', views.update_search_name),
    path('deleteSearch/<int:id>/', views.delete_search),
]

