from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', include('django.contrib.auth.urls')),

	path('login/', views.UserLoginView.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(), name='logout'),

	path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
	path(
		'password-reset-complete/',
		auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
		name='password_reset_complete'),
	path(
		'password-reset-confirm/<uidb64>/<token>/',
		auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
		name='password_reset_confirm'),
	path(
		'invalid_verify/',
		TemplateView.as_view(template_name='registration/invalid_verify.html'),
		name='invalid_verify'),
	path(
		'verify_email/<uidb64>/<token>/',
		views.EmailVerifyView.as_view(),
		name='verify_email'),
	path(
		'confirm_email/',
		TemplateView.as_view(template_name='registration/confirm_email.html'),
		name='confirm_email'),
	path('register/', views.RegisterView.as_view(), name='register'),
	path('profile/', views.profile, name='profile'),
]
