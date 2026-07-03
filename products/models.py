from django.db import models
from django.urls import reverse


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