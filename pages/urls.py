from django.urls import path, re_path
from .views import menu_items, login_user, dashboard_view, get_csrf_token, react_view, whoami, logout_user

urlpatterns = [
    path('api/menu/', menu_items, name='menu_items'),
    path('api/login/', login_user, name='login_user'),
    path('api/dashboard/', dashboard_view, name='dashboard'),
    path('csrf/', get_csrf_token, name='csrf_token'),
    path('api/whoami/', whoami, name='whoami'),
    path('api/logout/', logout_user, name='logout_user'),
    re_path(r'^.*$', react_view, name='react_view'), 
]

