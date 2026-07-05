from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import Address
from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem, Payment

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart.objects.prefetch_related(
            "items__product",
        ).select_related(
            "user",
        ),
        user=request.user,
    )

    if not cart.items.exists():

        return redirect("cart")

    addresses = Address.objects.filter(
        user=request.user
    ).order_by("-id")

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

        payment_method = request.POST.get(
            "payment_method"
        )

        if payment_method not in [ 'COD', 'ONLINE']:

            return redirect("checkout")

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
                    id=item.product.id
                ).update(
                    stock=F("stock") - item.quantity
                )


            OrderItem.objects.bulk_create(order_items)

            payment = Payment.objects.create(

                order=order,

                payment_method=payment_method,

                amount=order.total_amount,

            )

            if payment_method == "COD":

                payment.payment_status = "Pending"

                payment.save(
                    update_fields=["payment_status"]
                )

                order.status = "Pending"

                order.save(
                    update_fields=["status"]
                )

            else:

                payment.payment_status = "Pending"

                payment.save(
                    update_fields=["payment_status"]
                )

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
            "address",
            "payment",
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
    ).select_related(
        "address",
        "payment",
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
            "address",
            "payment",
        ).prefetch_related(
            "items"
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


@login_required
def cancel_order(request, order_number):

    order = get_object_or_404(

        Order.objects.select_related(
            "payment",
        ).prefetch_related(
            "items__product",
        ),

        order_number=order_number,

        user=request.user,

    )

    if order.status != "Pending":

        messages.error(
            request,
            "This order cannot be cancelled."
        )

        return redirect(
            "order_detail",
            order.order_number
        )

    with transaction.atomic():

        for item in order.items.all():

            Product.objects.filter(
                id=item.product.id
            ).update(
                stock=F("stock") + item.quantity
            )

        order.status = "Cancelled"
        order.save(
            update_fields=["status"]
        )

        if order.payment.payment_method == "ONLINE":

            order.payment.payment_status = "Refunded"

        else:

            order.payment.payment_status = "Pending"

        order.payment.save(
            update_fields=["payment_status"]
        )

    messages.success(
        request,
        "Order cancelled successfully."
    )

    return redirect(
        "order_detail",
        order.order_number
    )