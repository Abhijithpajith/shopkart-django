from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import product,variation
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    products = product.objects.get(id=product_id)  # get the product
    product_variation = []
    # if user is auhenticated
    if current_user.is_authenticated:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    vari = variation.objects.get(product=products, variation_category__iexact=key,
                                                 variation_value__iexact=value)
                    product_variation.append(vari)
                except:
                    pass

        is_cart_item_exists = cartitem.objects.filter(product=products, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = cartitem.objects.filter(product=products, user=current_user)
            # existing variation from database
            # current variation form product variation
            # item_id from database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = cartitem.objects.get(product=products, id=item_id,)
                item.quantity += 1
                item.save()
            else:

                item = cartitem.objects.create(product=products, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.save()
        else:
            cart_item = cartitem.objects.create(
                product=products,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
                cart_item.save()
        return redirect('cart')

    else:
        product_variation =[]
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    vari = variation.objects.get(product=products, variation_category__iexact=key,
                                                 variation_value__iexact=value)
                    product_variation.append(vari)
                except:
                    pass

        try:
            carts = cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in session
        except cart.DoesNotExist:
            carts = cart.objects.create(
                cart_id=_cart_id(request)
            )
            carts.save()
        is_cart_item_exists = cartitem.objects.filter(product=products, cart=carts).exists()
        if is_cart_item_exists:
            cart_item = cartitem.objects.filter(product=products, cart=carts)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = cartitem.objects.get(product=products, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = cartitem.objects.create(product=products, quantity=1, cart=carts)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = cartitem.objects.create(
                product=products,
                quantity=1,
                cart=carts,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request,product_id,cart_item_id):

    products = get_object_or_404(product, id=product_id, )
    try:
        if request.user.is_authenticated:
            cart_item = cartitem.objects.get(product=products, user=request.user, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            carts = cart.objects.get(cart_id=_cart_id(request))
            cart_item = cartitem.objects.get(product=products, cart=carts, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request,product_id,cart_item_id):

    products = get_object_or_404(product, id=product_id)
    if request.user.is_authenticated:
        cart_item= cartitem.objects.get(product=products,user=request.user,id=cart_item_id)
        cart_item.delete()
    else:
        carts = cart.objects.get(cart_id=_cart_id(request))
        cart_item = cartitem.objects.get(product=products, cart=carts, id=cart_item_id)
        cart_item.delete()
    return redirect('cart')


def cart_page(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = cartitem.objects.filter(user=request.user,is_active=True)
        else:
            carts=cart.objects.get(cart_id=_cart_id(request))
            cart_items=cartitem.objects.filter(cart=carts,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total= total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total':grand_total,


    }

    return render(request,'store/cart.html',context)

@login_required(login_url ='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = cartitem.objects.filter(user=request.user, is_active=True)
        else:
            carts = cart.objects.get(cart_id=_cart_id(request))
            cart_items = cartitem.objects.filter(cart=carts, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }

    return render(request,'store/checkout.html',context)

