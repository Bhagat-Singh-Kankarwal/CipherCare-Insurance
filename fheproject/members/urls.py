
from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register, name='register_user'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation_sent', views.activation_sent, name='activation_sent'),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name="authenticate/reset_password.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="authenticate/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/reset.html"), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/reset_password_complete.html"), name='password_reset_complete'),

]
