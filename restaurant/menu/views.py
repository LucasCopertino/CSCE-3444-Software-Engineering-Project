from django.shortcuts import render
from .models import Item, category

# Create your views here.

"""Overview: Render the menu page to the user
    Return: Returns a render response to the client 
"""
def menu_home(request):
    items = Item.objects.all() #put all food items in database in this single variable
    context = {'itms':items}


    return render(request, 'menu.html',context) 
def cat_g(request):
    cats = category.objects.all()

    return 0
