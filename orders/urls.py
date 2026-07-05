from django.urls import path

from . import views

urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "success/<uuid:order_number>/",
        views.order_success,
        name="order_success",
    ),

    path(
        "history/",
        views.order_history,
        name="order_history",
    ),

    path(
        "cancel/<uuid:order_number>/",
        views.cancel_order,
        name="cancel_order",
    ),

    path(
        "<uuid:order_number>/",
        views.order_detail,
        name="order_detail",
    ),

]
