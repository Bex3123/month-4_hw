from django.urls import path
from users import views
from users.views import profile_update_view

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('verify/<str:code>/', views.verify_view, name='verify'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view),
    path('profile/', views.profile_view),
    path('profile/update/', profile_update_view, name='profile_update'),
]
