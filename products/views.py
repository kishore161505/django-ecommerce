from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review,WishlistItem,Wishlist

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Exists, OuterRef

from .forms import ReviewForm
from cart.models import Cart, CartItem


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

    products = Product.objects.select_related(
        "category",
    ).annotate(
        average_rating=Avg("reviews__rating"),
        review_count=Count("reviews"),
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

        Product.objects.prefetch_related(
            "reviews__user",
        ).annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        ),

        slug=slug,

    )

    reviews = product.reviews.all()

    

    user_review = None

    if request.user.is_authenticated:

        user_review = Review.objects.filter(
            user=request.user,
            product=product,
        ).first()

    context = {

        "product": product,

        "reviews": reviews,

        "average_rating": product.average_rating,

        "total_reviews": product.review_count,

        "user_review": user_review,

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

@login_required
def add_review(request, slug):

    product = get_object_or_404(

        Product,

        slug=slug,

    )

    if Review.objects.filter(

        user=request.user,

        product=product,

    ).exists():

        return redirect(

            "product_detail",

            slug=slug,

        )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(

                commit=False,

            )

            review.user = request.user

            review.product = product

            review.save()

            return redirect(

                "product_detail",

                slug=slug,

            )

    else:

        form = ReviewForm()

    context = {

        "form": form,

        "product": product,

    }

    return render(

        request,

        "products/review_form.html",

        context,

    )

@login_required
def edit_review(request, review_id):

    review = get_object_or_404(

        Review,

        id=review_id,

        user=request.user,

    )

    if request.method == "POST":

        form = ReviewForm(

            request.POST,

            instance=review,

        )

        if form.is_valid():

            form.save()

            return redirect(

                "product_detail",

                slug=review.product.slug,

            )

    else:

        form = ReviewForm(

            instance=review,

        )

    context = {

        "form": form,

        "product": review.product,

    }

    return render(

        request,

        "products/review_form.html",

        context,

    )

@login_required
def delete_review(request, review_id):

    review = get_object_or_404(

        Review,

        id=review_id,

        user=request.user,

    )

    product_slug = review.product.slug

    review.delete()

    return redirect(

        "product_detail",

        slug=product_slug,

    )

@login_required
def wishlist(request):

    wishlist, created = Wishlist.objects.prefetch_related(
        "items__product",
    ).get_or_create(
        user=request.user
    )

    context = {

        "wishlist": wishlist,

    }

    return render(

        request,

        "products/wishlist.html",

        context,

    )

@login_required
def add_to_wishlist(request, slug):

    product = get_object_or_404(

        Product,

        slug=slug,

    )

    wishlist, created = Wishlist.objects.get_or_create(

        user=request.user,

    )

    if not WishlistItem.objects.filter(
        wishlist=wishlist,
        product=product,
    ).exists():

        WishlistItem.objects.create(
            wishlist=wishlist,
            product=product,
        )

    return redirect(

        "wishlist",

    )

@login_required
def remove_from_wishlist(request, item_id):

    item = get_object_or_404(

        WishlistItem,

        id=item_id,

        wishlist__user=request.user,

    )

    item.delete()

    return redirect(

        "wishlist",

    )

@login_required
def move_to_cart(request, item_id):

    wishlist_item = get_object_or_404(

        WishlistItem.objects.select_related(
            "product",
            "wishlist",
        ),

        id=item_id,

        wishlist__user=request.user,

    )

    cart, created = Cart.objects.get_or_create(

        user=request.user,

    )

    cart_item, created = CartItem.objects.get_or_create(

        cart=cart,

        product=wishlist_item.product,

        defaults={

            "quantity": 1,

            "price": wishlist_item.product.price,

        }

    )

    if not created:

        cart_item.quantity += 1

        cart_item.save(
            update_fields=["quantity"]
        )

    wishlist_item.delete()

    return redirect(

        "cart",

    )


