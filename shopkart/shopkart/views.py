from django.http import HttpResponse
from django.shortcuts import  render
from store.models import product,ReviewRating

def home(request):
    products = product.objects.all().filter(is_available=True).order_by('created_date')

    for pro in products:
        reviews= ReviewRating.objects.filter(product_id=pro.id,status=True)

    context={
        'products': products,
        'reviews':reviews

     }


    return render(request,'home.html',context)