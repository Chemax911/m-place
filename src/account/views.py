from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as \
	token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import UserCreationForm, ResetPasswordForm, UserAuthenticationForm, UserUpdateForm, \
	ProfileUpdateForm
from .utils import send_email_for_verify

User = get_user_model()


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
	template_name = 'users/password_reset.html'
	form_class = ResetPasswordForm
	email_template_name = 'users/password_reset_email.html'
	subject_template_name = 'users/password_reset_subject'
	success_message = "We've emailed you instructions for setting your password, " \
					  "if an account exists with the email you entered. You should receive them shortly." \
					  " If you don't receive an email, " \
					  "please make sure you've entered the address you registered with, and check your spam folder."
	success_url = reverse_lazy('home_page')


class RegisterView(View):
	""" User Register View """
	template_name = 'registration/register.html'

	def get(self, request):
		context = {
			'form': UserCreationForm()
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=password)
			send_email_for_verify(request, user)
			return redirect('confirm_email')
		context = {
			'form': form
		}
		return render(request, self.template_name, context)


class UserLoginView(LoginView):
	""" User Login View """

	form_class = UserAuthenticationForm
	template_name = 'registration/login.html'


class EmailVerifyView(View):
	""" Email Verify View """

	def get(self, request, uidb64, token):
		user = self.get_user(uidb64)

		if user is not None and token_generator.check_token(user, token):
			user.email_verify = True
			user.save()
			login(request, user)
			return redirect('home_page')
		return redirect('invalid_verify')

	@staticmethod
	def get_user(uidb64):
		try:
			# urlsafe_base64_decode() decodes to bytestring
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (
				TypeError, ValueError, OverflowError,
				User.DoesNotExist, ValidationError):
			user = None
		return user


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(
			request.POST,
			request.FILES,
			instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'users/profile.html', context)
