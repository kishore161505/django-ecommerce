from django.contrib import admin

from .models import Category, Product, Review, Wishlist, WishlistItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "is_available",
    )

    list_filter = (
        "category",
        "is_available",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (

        "product",

        "user",

        "rating",

        "created_at",

    )

    list_filter = (

        "rating",

        "created_at",

    )

    search_fields = (

        "product__name",

        "user__username",

    )

    readonly_fields = (

        "created_at",

        "updated_at",

    )

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (

        "user",

        "created_at",

    )

    search_fields = (

        "user__username",

    )

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):

    list_display = (

        "wishlist",

        "product",

        "created_at",

    )

    search_fields = (

        "wishlist__user__username",

        "product__name",

    )

    list_filter = (

        "created_at",

    )
