from django.urls import path

from . import views

urlpatterns = [

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

    path(
        "addresses/",
        views.address_list,
        name="address_list",
    ),

    path(
        "addresses/add/",
        views.add_address,
        name="add_address",
    ),

    path(
        "addresses/<int:pk>/edit/",
        views.edit_address,
        name="edit_address",
    ),

    path(
        "addresses/<int:pk>/delete/",
        views.delete_address,
        name="delete_address",
    ),

]

