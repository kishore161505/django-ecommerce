from django.shortcuts import render, get_object_or_404

from .models import Category, Product

from django.core.paginator import Paginator

from django.db.models import Q


def home(request):

    categories = Category.objects.filter(
        is_active=True
    )

    if not categories.exists():

        categories = []

    products = Product.objects.filter(
        is_available=True
    ).select_related(
        "category"
    ).only(
        "id",
        "name",
        "slug",
        "price",
        "image",
        "category__name"
    ).order_by(
        "-created_at"
    )[:8]

    context = {
        "categories": categories,
        "products": products,
    }

    return render(
        request,
        "products/home.html",
        context,
    )

def product_list(request):

    query = request.GET.get("q")

    products = Product.objects.filter(
        is_available=True
    )

    has_products = products.exists()

    if query:

        products = products.filter(

            Q(name__icontains=query) |

            Q(brand__icontains=query)

        )

    paginator = Paginator(
        products,
        8
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "page_obj": page_obj,

        "query": query,

        "has_products": has_products,

    }

    return render(

        request,

        "products/product_list.html",

        context,

    )


def product_detail(request, slug):



    product = get_object_or_404(

        Product.objects.select_related(
            "category"
        ),

        slug=slug,

        is_available=True,

    )

    

    context = {
        "product": product,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )


def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_available=True
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }

    return render(
        request,
        "products/category_products.html",
        context,
    )