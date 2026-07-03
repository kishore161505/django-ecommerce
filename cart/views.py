from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartItem
from products.models import Product

from django.db.models import (
    F,
    Sum,
    DecimalField,
    ExpressionWrapper,
)

@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related(
        "product",
        "product__category",
    ).order_by(
        "created_at"
    )

    context = {

        "cart": cart,

        "items": items,

    }

    return render(
        request,
        "cart/cart.html",
        context,
    )

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    if product.stock <= 0:

        return redirect("product_detail", slug=product.slug)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(

        cart=cart,

        product=product,

        defaults={
            "price": product.price
        }

    )

    if not created:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1

            cart_item.save(  update_fields=["quantity"] )

    return redirect("cart")

@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    if item.quantity < item.product.stock:

        item.quantity = F("quantity") + 1

        item.save(
            update_fields=["quantity"]
        )

        item.refresh_from_db()

    return redirect("cart")

@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    if item.quantity > 1:

        item.quantity = F("quantity") - 1

        item.save(
            update_fields=["quantity"]
        )

        item.refresh_from_db()

    else:

        item.delete()

    return redirect("cart")

@login_required
def remove_item(request, item_id):

    item = get_object_or_404(

        CartItem,

        id=item_id,

        cart__user=request.user

    )

    item.delete()

    return redirect("cart")

@login_required
def clear_cart(request):

    cart = get_object_or_404(

        Cart,

        user=request.user

    )

    cart.items.all().delete()

    return redirect("cart")