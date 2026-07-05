import uuid

from decimal import Decimal

from django.conf import settings
from django.db import models

from accounts.models import Address
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (

        ("Pending", "Pending"),

        ("Processing", "Processing"),

        ("Shipped", "Shipped"),

        ("Delivered", "Delivered"),

        ("Cancelled", "Cancelled"),

    )

    order_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return str(self.order_number)
    
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    product_name = models.CharField(
        max_length=200,
    )

    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:

        ordering = ["id"]

    def __str__(self):

        return self.product_name
    

class Payment(models.Model):

    PAYMENT_METHODS = (

        ("COD", "Cash On Delivery"),

        ("ONLINE", "Online Payment"),

    )

    PAYMENT_STATUS = (

        ("Pending", "Pending"),

        ("Completed", "Completed"),

        ("Failed", "Failed"),

        ("Refunded", "Refunded"),

    )

    order = models.OneToOneField(

        Order,

        on_delete=models.CASCADE,

        related_name="payment",

    )

    payment_method = models.CharField(

        max_length=20,

        choices=PAYMENT_METHODS,

    )

    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS,

        default="Pending",

    )

    transaction_id = models.CharField(

        max_length=100,

        blank=True,

        null=True,

    )

    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2,

    )

    paid_at = models.DateTimeField(

        blank=True,

        null=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    def __str__(self):

        return f"{self.order.order_number} - {self.payment_method}"