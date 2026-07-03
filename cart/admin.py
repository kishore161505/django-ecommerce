from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):

    model = CartItem

    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_items",
        "total_amount",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    inlines = [
        CartItemInline,
    ]

    def total_items(self, obj):

        return obj.total_quantity

    def total_amount(self, obj):

        return obj.total_price


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
        "price",
        "subtotal_display",
    )

    list_filter = (
        "product__category",
    )

    search_fields = (
        "product__name",
    )

    def subtotal_display(self, obj):

        return obj.subtotal