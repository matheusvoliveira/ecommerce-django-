from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from .models import Product
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from .utils.adress_utils import cep_locater
from .utils.credit_card_utils import credit_card_validator
# Create your views here.


def index(request):
    return render(request, 'index.html')


class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('create_product')

    def form_valid(self, form):
        messages.success(self.request, 'The Product was created successfully')
        return super().form_valid(form)


class BuyerProductList(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'products/buyer_product_list.html'


class SellerProductList(ListView):
    model = Product
    context_object_name = 'product_list'


class ProductDetail(DetailView):
    model = Product


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('list_product')

class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('list_product')

def calculate_total(cart_items):
    total_cost = sum(item.product.price for item in cart_items)
    return total_cost


def add_to_cart(request, product_id):
    
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.create(user=request.user, product=product)

    cart.save()

    cart_items = Cart.objects.all()
    total_cost = calculate_total(cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost
    }
    return render(request, 'cart/shopping_cart.html', context)

def remove_from_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    cart_items = Cart.objects.all()
    total_cost = calculate_total(cart_items)

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart/shopping_cart.html', context)

def remove_all_from_cart(request):
    full_cart = Cart.objects.all()
    full_cart.delete()

    cart_items = Cart.objects.all()

    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart/shopping_cart.html', context)


def shopping_cart(request):
    cart_items = Cart.objects.all()
    total_cost = calculate_total(cart_items)

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart/shopping_cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def adress_completer(request):

    if request.method == 'POST':
        cep = request.POST.get('cep')
        adress_data = cep_locater(cep)

        if len(cep) != 8 or adress_data.get('erro'):
            messages.warning(request, 'This CEP is invalid!')
    

        house_number = request.POST.get('numero_casa')
        street = request.POST.get('logradouro')
        neighborhood = request.POST.get('bairro')
        state = request.POST.get('uf')
        city = request.POST.get('localidade')
        context = {
            'adress_data': adress_data,
            'numero_casa': house_number,
            'logradouro': street,
            'bairro': neighborhood,
            'uf': state,
            'localidade': city
        }
        return render(request, 'paying_send/cep_locater.html', context)
    
    return render(request, 'paying_send/cep_locater.html')


def credit_card(request):
    cc_number = request.POST.get('cc_number')

    if request.method == 'POST':
        
        credit_card_verify = credit_card_validator(cc_number)
        if credit_card_verify == False:
            messages.warning(request, 'This credit card number is invalid!')
        else:
            return redirect('cep_locater')
        
    cvc = request.POST.get('cvc')
    expiration_date = request.POST.get('expiration_date')
    name = request.POST.get('name')




    context = {
        'cc_number': cc_number,
        'cvc': cvc,
        'expiration_date': expiration_date,
        'name': name
    }

    return render(request, 'paying_send/credit_card.html', context)


def final_screen(request):
    return render(request,'paying_send/final_screen.html')