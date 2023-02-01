from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from school.models import Abonement
from .basket import Basket


@login_required()
def basket_summary(request):
    return render(request, 'basket/basket_summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Abonement, id=product_id)
        basket.add(product=product, quantity=product_qty)

        basket_qty = len(basket)
        response = JsonResponse({'quantity': basket_qty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'delete':
        product_id = request.POST.get('productid')
        print(len(basket))
        basket.delete(product_id=product_id)
        basket_total = basket.get_total_price()
        basket_quantity = len(basket)
        response = JsonResponse({'quantity': basket_quantity,
                                 'total': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'update':
        product_id = request.POST.get('productid')
        product_qty = int(request.POST.get('productqty'))

        basket.update(product_id=product_id, quantity=product_qty)

        basket_quantity = len(basket)
        basket_total = basket.get_total_price()
        response = JsonResponse({'quantity': basket_quantity,
                                 'total': basket_total})
        return response
