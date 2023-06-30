from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from category.models import category
from cartapp.models import cartitem
from cartapp.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.

def store_page(request,category_slug=None):
    cat=None
    pro=None
    if category_slug !=None:
        cat=get_object_or_404(category,slug=category_slug)
        pro=product.objects.filter(category=cat,is_available=True)
        paginator = Paginator(pro, 1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page, )
        product_count=pro.count()
    else:

        pro = product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(pro,3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page,)
        product_count=pro.count()
    return  render(request,'store/store.html',{'pro':paged_product,'product_count':product_count,})

def product_details(request,category_slug,product_slug):
    try:
        single_product=product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    return render(request,'store/product_details.html',{'single_product':single_product,'in_cart':in_cart})


def search(request):
    pro=None
    product_count=None
    if 'q' in request.GET:
        keyword=request.GET['q']
        if keyword:
            pro = product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count = pro.count()
    return render(request,'store/store.html',{'pro':pro,'products_count':product_count})