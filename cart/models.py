from decimal import Decimal

from django.conf import settings
from django.db import models

from django.db.models import (
    F,
    Sum,
    DecimalField,
    ExpressionWrapper,
)

from products.models import Product


class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-updated_at"]

    def __str__(self):

        return f"{self.user.username}'s Cart"

    @property
    def total_price(self):

        total = self.items.aggregate(

            total=Sum(

                ExpressionWrapper(

                    F("price") * F("quantity"),

                    output_field=DecimalField()

                )

            )

        )["total"]

        return total or Decimal("0.00")

    @property
    def total_quantity(self):

        total = self.items.aggregate(

            total=Sum("quantity")

        )["total"]

        return total or 0


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["created_at"]

        unique_together = ("cart", "product")

    def __str__(self):

        return self.product.name

    @property
    def subtotal(self):

        return self.price * self.quantity