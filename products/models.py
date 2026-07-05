from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=120, unique=True)

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["name"]

        verbose_name = "Category"

        verbose_name_plural = "Categories"

    def __str__(self):

        return self.name

    def get_absolute_url(self):

        return reverse(
            "category_products",
            args=[self.slug]
        )


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    sku = models.CharField(max_length=50, unique=True)

    brand = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=220,
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/"
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return self.name

    def get_absolute_url(self):

        return reverse(
            "product_detail",
            args=[self.slug]
        )
    

class Review(models.Model):

    RATING_CHOICES = (

        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),

    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="reviews",

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        related_name="reviews",

    )

    rating = models.PositiveSmallIntegerField(

        choices=RATING_CHOICES,

    )

    review = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=["user", "product"],

                name="unique_product_review",

            )

        ]

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"
    
class Wishlist(models.Model):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="wishlist",

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    def __str__(self):

        return f"{self.user.username}'s Wishlist"
    
class WishlistItem(models.Model):

    wishlist = models.ForeignKey(

        Wishlist,

        on_delete=models.CASCADE,

        related_name="items",

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        related_name="wishlist_items",

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=[

                    "wishlist",

                    "product",

                ],

                name="unique_wishlist_product",

            )

        ]

    def __str__(self):

        return f"{self.product.name}"