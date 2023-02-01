from django.urls import path
from .views import basket_summary, basket_add

urlpatterns = [
    path('', basket_summary, name='basket'),
    path('add/', basket_add, name='basket_add')
]
