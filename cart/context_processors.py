from .models import Cart


def cart_data(request):

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        return {

            "cart": cart,

            "cart_count": cart.total_quantity,

        }

    return {

        "cart": None,

        "cart_count": 0,

    }