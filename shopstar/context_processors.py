from product.models import Category
from order_detail.models import Order

def categories(request):
    return {
        'categories': Category.objects.all(),
    }

def cartitems(request):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer,complete=False).exists()
        if order:
            order = Order.objects.get(customer=customer,complete=False)
            cartItems = order.get_total_item
        else:
            cartItems = 0
    else:
        cartItems = 0
    return {'cartItems':cartItems}