from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "products/",
        views.product_list,
        name="product_list",
    ),

    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "category/<slug:slug>/",
        views.category_products,
        name="category_products",
    ),

    path(
    "<slug:slug>/review/",
    views.add_review,
    name="add_review",
    ),

    path(
        "review/<int:review_id>/edit/",
        views.edit_review,
        name="edit_review",
    ),

    path(
        "review/<int:review_id>/delete/",
        views.delete_review,
        name="delete_review",
    ),

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist",
    ),

    path(
        "wishlist/add/<slug:slug>/",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),

    path(
        "wishlist/remove/<int:item_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),

    path(
        "wishlist/move/<int:item_id>/",
        views.move_to_cart,
        name="move_to_cart",
    ),

]