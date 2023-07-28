from django.shortcuts import render,redirect
from django.http import  HttpResponse,JsonResponse
from cartapp.models import cartitem
from .forms import orderform
from .models import  Order, payment,orderproduct
import datetime
import  razorpay
from shopkart.settings import RAZORPAY_API_KEY_ID,RAZORPAY_API_KEY_SECRET
import json
from store.models import product
from django.core.mail import  EmailMessage
from django.template.loader import render_to_string



# Create your views here.
def place_order(request,total=0,quantity=0):
    current_user = request.user

    # if the count is less than or equal to 0 thn the redirect back to shop

    cart_items= cartitem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('store')

    tax = 0
    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = orderform(request.POST)
        if form.is_valid():
            data  = Order()
            data.user = current_user
            print(data.user)
            data.first_name =form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state= form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total= grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt =int(datetime.date.today().strftime('%d'))
            mt =int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%y%d%m')
            order_number =current_date + str(data.id)
            data.order_number =order_number
            data.save()

            client = razorpay.Client(auth=(RAZORPAY_API_KEY_ID, RAZORPAY_API_KEY_SECRET))
            DATA= {"amount":grand_total*100,"currency":"INR","payment_capture":1}
            payment_order=client.order.create(data=DATA)
            print(payment_order)

            payment_order_id=payment_order['id']


            order = Order.objects.get(user=current_user,is_ordered =False,order_number = order_number)
            context = {
                'order':order,
                'cart_items': cart_items,
                'total' : total,
                'tax':tax,
                'grand_total': grand_total,
                'api_key_id':RAZORPAY_API_KEY_ID,
                'order_id':payment_order_id,


            }

            return render(request,'orders/payments.html',context)
        else:
            return HttpResponse('failed')

    else:
        return redirect('checkout')

def payments(request):
    body= json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number =body['orderID'])
    #STORE TRANSACTION DETAILS INSIDE PAYMENT METHOD
    Payment = payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid =order.order_total,
        status = body['status']
    )
    Payment.save()
    order.payment = Payment
    order.is_ordered=True
    order.save()
    # MOVE  the cat items to order product table
    cartitems = cartitem.objects.filter(user=request.user)
    for item in cartitems:
        orderprod = orderproduct()
        orderprod.order_id =order.id
        orderprod.payment=Payment
        orderprod.user_id=request.user.id
        orderprod.product_id=item.product_id
        orderprod.quantity=item.quantity

        orderprod.product_price =item.product.price
        orderprod.ordered =True
        orderprod.save()
        print(orderprod)

        cart_item =cartitem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderprod = orderproduct.objects.get(id=orderprod.id)
        orderprod.variations.set(product_variation)
        orderprod.save()
        # reduce the quantity of the sold products

        Product = product.objects.get(id=item.product_id)
        Product.stock -=item.quantity
        Product.save()


    # clear cart
    cartitem.objects.filter(user=request.user).delete()

    # send order recived email to customer

    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order,

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # send order number and transaction id back to sendData method via jsonResponse


    data={
        'order_number': order.order_number,
        'transID':Payment.payment_id
    }
    return JsonResponse(data)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID =request.GET.get('payment_id')
    subtotal=0

    try:
        order =Order.objects.get(order_number =order_number,is_ordered=True)
        ordered_products =orderproduct.objects.filter(order_id=order.id)
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payments =payment.objects.get(payment_id=transID)

        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payments.payment_id,
            'payments':payments,
            'subtotal':subtotal

        }
        return render(request,'orders/order_complete.html',context)
    except (payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
