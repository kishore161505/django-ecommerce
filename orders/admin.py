from django.contrib import admin

from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (

        "product",

        "product_name",

        "product_price",

        "quantity",

        "subtotal",

    )

    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "order_number",

        "user",

        "status",

        "total_amount",

        "created_at",

    )

    list_filter = (

        "status",

        "created_at",

    )

    search_fields = (

        "order_number",

        "user__username",

        "user__email",

    )

    readonly_fields = (

        "order_number",

        "created_at",

        "updated_at",

    )

    inlines = [

        OrderItemInline,

    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "product_name",

        "quantity",

        "product_price",

        "subtotal",

    )

    search_fields = (

        "product_name",

    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "payment_method",

        "payment_status",

        "amount",

        "transaction_id",

        "created_at",

    )

    list_filter = (

        "payment_method",

        "payment_status",

        "created_at",

    )

    search_fields = (

        "order__order_number",

        "transaction_id",

        "order__user__username",

    )

    readonly_fields = (

        "amount",

        "payment_method",

        "created_at",

        "updated_at",

    )