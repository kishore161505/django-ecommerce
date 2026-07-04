from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Address
from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart.objects.prefetch_related(
            "items__product",
            "items__product__category",
        ),
        user=request.user
    )

    if not cart.items.exists():

        return redirect("cart")

    addresses = Address.objects.filter(
        user=request.user
    )

    if not addresses.exists():

        return redirect(
            "address_list"
        )

    if request.method == "POST":

        address_id = request.POST.get("address")

        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user
        )

        with transaction.atomic():

            order = Order.objects.create(

                user=request.user,

                address=address,

                total_amount=cart.total_price,

            )

            order_items = []

            for item in cart.items.all():

                product = item.product

                if product.stock < item.quantity:

                    transaction.set_rollback(True)

                    return redirect("cart")
                
                order_items.append(


                    OrderItem(

                        order=order,

                        product=product,

                        product_name=product.name,

                        product_price=item.price,

                        quantity=item.quantity,

                        subtotal=item.subtotal,

                    )
                )

                

                Product.objects.filter(
                    id=product.id
                ).update(
                    stock=F("stock") - item.quantity
                )

            OrderItem.objects.bulk_create(order_items)

            cart.items.all().delete()

        return redirect(
            "order_success",
            order.order_number
        )

    context = {

        "cart": cart,

        "addresses": addresses,

    }

    return render(

        request,

        "orders/checkout.html",

        context,

    )


@login_required
def order_success(request, order_number):

    order = get_object_or_404(

        Order.objects.select_related(
            "address"
        ),

        order_number=order_number,

        user=request.user,

    )

    context = {

        "order": order,

    }

    return render(

        request,

        "orders/order_success.html",

        context,

    )

@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).only(
        "order_number",
        "status",
        "total_amount",
        "created_at",
        "address",
    ).select_related(
        "address"
    ).order_by(
        "-created_at"
    )

    context = {

        "orders": orders,

    }

    return render(

        request,

        "orders/order_history.html",

        context,

    )

@login_required
def order_detail(request, order_number):

    order = get_object_or_404(

        Order.objects.select_related(
            "address"
        ).prefetch_related(
            "items"
        ).only(
            "order_number",
            "status",
            "total_amount",
            "created_at",
            "address",
        ),

        order_number=order_number,

        user=request.user,

    )

    context = {

        "order": order,

    }

    return render(

        request,

        "orders/order_detail.html",

        context,

    )
