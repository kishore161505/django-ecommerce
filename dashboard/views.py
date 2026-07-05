from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper, Avg, Prefetch
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from orders.models import Order, OrderItem
from products.models import Category, Product, Review

User = get_user_model()


@staff_member_required
def dashboard(request):

    registered_users = User.objects.count()

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_reviews = Review.objects.count()

    total_orders = Order.objects.count()

    users_with_orders = User.objects.filter(

        orders__isnull=False,

    ).distinct().count()

    users_without_orders = User.objects.filter(

        orders__isnull=True,

    ).count()

    revenue = Order.objects.filter(

        status__in=[

            "Pending",

            "Shipped",

            "Delivered",

        ]

    ).aggregate(

        total=Sum("total_amount")

    )["total"] or 0

    monthly_revenue = (

        Order.objects.filter(

            status__in=[

                "Pending",

                "Shipped",

                "Delivered",

            ]

        )

        .annotate(

            month=TruncMonth("created_at")

        )

        .values("month")

        .annotate(

            revenue=Sum("total_amount")

        )

        .order_by("month")

    )

    monthly_orders = (

        Order.objects.annotate(

            month=TruncMonth("created_at")

        )

        .values("month")

        .annotate(

            total_orders=Count("id")

        )

        .order_by("month")

    )

    best_selling_products = (

        OrderItem.objects.values(

            "product__name"

        )

        .annotate(

            total_sold=Sum("quantity")

        )

        .order_by("-total_sold")[:5]

    )

    top_customers = User.objects.only(

        "username",

        "email",

    ).annotate(

        total_orders=Count(

            "orders",

            distinct=True,

        ),

        total_spent=Sum(

            "orders__total_amount",

        ),

    ).filter(

        total_orders__gt=0,

    ).order_by(

        "-total_spent",

    )[:5]

    low_stock_products = Product.objects.select_related(

        "category",

    ).only(

        "name",

        "stock",

        "category__name",

    ).filter(

        stock__gt=0,

        stock__lte=10,

    ).order_by(

        "stock",

    )

    out_of_stock_products = Product.objects.select_related(

        "category",

    ).only(

        "name",

        "category__name",

    ).filter(

        stock=0,

    ).order_by(

        "name",

)

    inventory_value = Product.objects.aggregate(

        total=Sum(

            ExpressionWrapper(

                F("price") * F("stock"),

                output_field=DecimalField(

                    max_digits=12,

                    decimal_places=2,

                ),

            )

        )

    )["total"] or 0

    recent_products = Product.objects.select_related(

        "category",

    ).only(

        "name",

        "price",

        "stock",

        "created_at",

        "category__name",

    ).order_by(

        "-created_at",

    )[:5]

    most_active_customers = User.objects.only(

        "username",

        "email",

    ).annotate(

        total_orders=Count(

            "orders",

            distinct=True,

        ),

        total_spent=Sum(

            "orders__total_amount",

        ),

    ).filter(

        total_orders__gt=0,

    ).order_by(

        "-total_orders",

        "-total_spent",

    )[:10]


    context = {

        "total_users": total_users,

        "total_products": total_products,

        "total_categories": total_categories,

        "total_reviews": total_reviews,

        "total_orders": total_orders,

        "total_revenue": revenue,

        "monthly_revenue": monthly_revenue,

        "monthly_orders": monthly_orders,

        "best_selling_products": best_selling_products,

        "top_customers": top_customers,

        "low_stock_products": low_stock_products,

        "out_of_stock_products": out_of_stock_products,

        "inventory_value": inventory_value,

        "recent_products": recent_products,

        "registered_users": registered_users,

        "users_with_orders": users_with_orders,

        "users_without_orders": users_without_orders,

        "most_active_customers": most_active_customers,

    }

    return render(

        request,

        "dashboard/dashboard.html",

        context,

    )