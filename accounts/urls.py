from django.urls import path

from . import auth_views
from . import views

urlpatterns = [
    # Register & Login URLs
    path('register/', auth_views.register_page, name="register"),
    path('login/', auth_views.login_page, name="login"),
    path('logout/', auth_views.logout_page, name="logout"),

    path('forgot_password/', auth_views.forgot_password, name="forgot_password"),

]
