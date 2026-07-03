from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from .forms import AddressForm
from .models import Address

from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def register(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("profile")

    else:
        form = UserRegisterForm()

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/register.html",
        context,
    )


def user_login(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("profile")

    else:

        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/login.html",
        context,
    )


@login_required
def user_logout(request):

    logout(request)

    return redirect("login")


@login_required
def profile(request):

    context = {
        "user": request.user
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    context = {

        "user_form": user_form,
        "profile_form": profile_form

    }

    return render(
        request,
        "accounts/profile_edit.html",
        context,
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/password_change.html",
        context,
    )

@login_required
def address_list(request):
    addresses = Address.objects.filter(
        user=request.user
    )

    context = {
        "addresses": addresses
    }

    return render(request,"accounts/address_list.html",context)

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)

            address.user = request.user

            address.save()

            return redirect("address_list")
        
        else:

            form = AddressForm()

        context = {
            "form": form
        }

        return render(
            request,
            "accounts/address_form.html",
            context,
        )
    
@login_required
def edit_address(request, pk):

    address = get_object_or_404(
        Address,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = AddressForm(
            request.POST,
            instance=address
        )

        if form.is_valid():

            form.save()

            return redirect("address_list")

    else:

        form = AddressForm(
            instance=address
        )

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/address_form.html",
        context,
    )

@login_required
def delete_address(request, pk):

    address = get_object_or_404(
        Address,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        address.delete()

        return redirect("address_list")

    context = {
        "address": address
    }

    return render(
        request,
        "accounts/address_delete.html",
        context,
    )