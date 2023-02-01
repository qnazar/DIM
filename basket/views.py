from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from school.models import Abonement
from .basket import Basket


def basket_summary(request):
    return render(request, 'basket/basket_summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('productid')
        product = get_object_or_404(Abonement, id=int(product_id))
        basket.add(product=product)
        response = JsonResponse({'test': 'data'})
        return response
