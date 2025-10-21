from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import re
# Create your views here.


def dashboard(request):
    product=Product.objects.all()

    # search code
    search_item=request.GET.get('item_name' ,'')
    if search_item!=" " and search_item!=None:
        product=product.filter(name__icontains=search_item.strip())

    # paginator code
    pagination=Paginator(product,4)
    page=request.GET.get('page')
    product=pagination.get_page(page)

     


    return render(request,'shop/dashboard.html',{'product':product})


def detail_view_page(request,pk):
    product=Product.objects.get(pk=pk)
    
    return render(request,'shop/detail_view.html',{'product':product})