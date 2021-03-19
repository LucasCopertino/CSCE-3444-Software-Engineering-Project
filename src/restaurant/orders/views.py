from django.shortcuts import render
# Create your views here.
def cart(request):
    return render( request,'cart_page.html')

def start_payment(request):
    return render (request, 'payment_1_start.html')


def split_payment(request):
    return render(request, 'payment_2_split_choice.html')

def how_many_split(request):
    return render (request, 'payment_3_how_many_split.html')

def choose_method(request):
    return render (request, 'payment_4_choose_method.html')
def cash_payment(request):
    return render(request, 'payment_5B_cash.html')

def card_payment(request):
    return render(request, 'payment_5A_card.html')
    