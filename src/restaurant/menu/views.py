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
def cat_g(request, category_id):
    categories= category.objects.get(pk=category_id)
    cats = category.objects.all()
    category_posts = Item.objects.filter(cat=categories)
    return render(request, 'menu.html', {'cats': cats,'categories':categories,'category_posts':category_posts})


    #return 0
