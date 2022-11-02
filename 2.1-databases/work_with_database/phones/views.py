from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sorting = request.GET.get('sort')
    if sorting == 'name':
        phone_obj = Phone.objects.order_by('name')
    elif sorting == 'min_price':
        phone_obj = Phone.objects.order_by('price')
    elif sorting == 'max_price':
        phone_obj = Phone.objects.order_by('price').reverse()
    else:
        phone_obj = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phone_obj}
    return render(request, template, context)


def show_product(request, slug):
    phone_obj = Phone.objects.filter(slug=slug)[0]
    print(phone_obj)
    template = 'product.html'
    context = {'phone': phone_obj}
    return render(request, template, context)
