from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Address


class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    email = forms.EmailField()

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = (
            "phone_number",
            "profile_image",
            "date_of_birth",
        )


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        exclude = (
            "user",
            "created_at",
        )