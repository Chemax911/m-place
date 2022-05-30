from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
	UserCreationForm as CreationForm,
	PasswordResetForm,
	AuthenticationForm,
	UsernameField,
	UserChangeForm
)
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import NumberInput
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .models import Profile, City
from .utils import send_email_for_verify

User = get_user_model()


class UserAdminCreationForm(CreationForm):
	""" User Admin Creation Form """

	email = forms.EmailField(
		label=_('Email'), max_length=254,
		widget=forms.EmailInput(
			attrs={'autocomplete': 'email'}))

	class Meta:
		model = get_user_model()
		fields = ('email', 'username')


class UserAdminChangeForm(UserChangeForm):
	""" User Admin Change Form """

	class Meta:
		model = get_user_model()
		fields = ('email', 'username')



class UserAuthenticationForm(AuthenticationForm):
	""" User Authentication Form """

	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				'autocomplete': 'email',
				'autofocus': True
			}
		)
	)

	class Meta:
		model = User
		fields = ('email', 'username')

	def __init__(self, *args, **kwargs):
		super(AuthenticationForm, self).__init__(*args, **kwargs)

		for fieldname, field in self.fields.items():
			field.label = False
		
		self.fields['email'].widget.attrs.update(
			{
				'placeholder': 'email@example.com',
				'class': 'form-control'
			}
		)
		self.fields['password'].widget.attrs.update({
			'class': 'form-control'})

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		email_verify = self.cleaned_data.get('email_verify')

		if username is not None and password:
			self.user_cache = authenticate(
				self.request,
				username=username,
				password=password,
				email_verify=email_verify
			)
			if not self.user_cache.email_verify:
				send_email_for_verify(self.request, self.user_cache)
				raise ValidationError(
					_('Email not verify, check your email'),
					code='invalid_login'
				)

			if self.user_cache is None:
				raise self.get_invalid_login_error()
			else:
				self.confirm_login_allowed(self.user_cache)

		return self.cleaned_data



# class UserAuthenticationForm(AuthenticationForm):
# 	""" User Authentication Form """

# 	email = forms.EmailField(
# 		widget=forms.EmailInput(
# 			attrs={
# 				'placeholder': 'email@example.com',
# 				'autocomplete': 'email',
# 				'class': 'form-control',
# 				'autofocus': True}))
	
# 	class Meta:
# 		model = get_user_model()
# 		fields = ('email',)

# 	def __init__(self, *args, **kwargs):
# 		super(UserAuthenticationForm, self).__init__(*args, **kwargs)

# 		for fieldname, field in self.fields.items():
# 			field.label = False

# 		self.fields['password'].widget.attrs.update({'class': 'form-control'})
# 		self.fields['email'].widget.attrs.update({'class': 'form-control'})

# 	def clean(self):
# 		email = self.cleaned_data.get('email')
# 		password = self.cleaned_data.get('password')
# 		email_verify = self.cleaned_data.get('email_verify')

# 		if email is not None and password:
# 			self.user_cache = authenticate(
# 				self.request,
# 				username=email,
# 				password=password,
# 				email_verify=email_verify
# 			)
# 			if not self.user_cache.email_verify:
# 				send_email_for_verify(self.request, self.user_cache)
# 				raise ValidationError(
# 					_('Email not verify, check your email'),
# 					code='invalid_login',
# 				)

# 			if self.user_cache is None:
# 				raise self.get_invalid_login_error()
# 			else:
# 				self.confirm_login_allowed(self.user_cache)

# 		return self.cleaned_data


class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(
		label='', max_length=254, widget=forms.EmailInput(
			attrs={
				'placeholder': 'email@example.com',
				'autocomplete': 'email',
				'class': 'form-control'}))


class UserCreationForm(CreationForm):
	email = forms.EmailField(
		max_length=254, required=True, widget=forms.EmailInput(
			attrs={
				'placeholder': 'email@example.com',
				'autocomplete': 'email',
				'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email')

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)

		for fieldname, field in self.fields.items():
			field.label = False

		self.fields['username'].widget.attrs.update({
			'placeholder': 'например, Иван Иванович',
			'class': 'form-control'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(
		max_length=254, required=False, widget=forms.EmailInput(
			attrs={
				'placeholder': 'email@example.com',
				'autocomplete': 'email',
				'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)

		for fieldname, field in self.fields.items():
			field.label = False

		self.fields['first_name'].widget.attrs.update({
			'placeholder': 'Имя',
			'class': 'form-control'})
		self.fields['last_name'].widget.attrs.update({
			'placeholder': 'Фамилия',
			'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):

	GENDER_MALE = 1
	GENDER_FEMALE = 2
	GENDER_CHOICES = [
		(GENDER_MALE, _('Мужчина')),
		(GENDER_FEMALE, _('Женщина')),
	]

	city = forms.ModelChoiceField(required=False, queryset=City.objects.all())
	gender = forms.ChoiceField(required=False, widget=forms.RadioSelect(), choices=GENDER_CHOICES)
	birthday = forms.DateField(
		required=False,
		widget=NumberInput(
			attrs={
				'type': 'date',
				'class': 'form-control form-control-md'}))
	phone = PhoneNumberField(required=False, widget=forms.TextInput())
	image = forms.ImageField(required=False, widget=forms.FileInput())

	class Meta:
		model = Profile
		fields = ('image', 'gender', 'birthday', 'city', 'phone')

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)

		for fieldname, field in self.fields.items():
			field.label = False

		self.fields['image'].widget.attrs.update({'class': 'img_upload'})
		self.fields['gender'].widget.attrs.update({'class': 'marker'})
		self.fields['city'].widget.attrs.update({'class': 'form-control'})
		self.fields['phone'].widget.attrs.update({
			'placeholder': _('+38(093)12-34-567'),
			'class': 'form-control'})

# class ProfileAdminCreationForm(CreationForm):
# 	""" User Admin Creation Form """
#
# 	email = forms.EmailField(
# 		label=_('Email'), max_length=254,
# 		widget=forms.EmailInput(
# 			attrs={'autocomplete': 'email'}))
#
# 	class Meta:
# 		model = get_user_model()
# 		fields = ('email', 'username')
#
#
# class ProfileAdminChangeForm(UserChangeForm):
# 	""" User Admin Change Form """
#
# 	class Meta:
# 		model = get_user_model()
# 		fields = ('email', 'username')
