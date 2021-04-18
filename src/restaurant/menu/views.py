from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item, category
from accounts.decorators import allowed_users, unauthenticated_user
from django.contrib.auth.models import Group


# Create your views here.

"""Overview: Render the menu page to the user
    Return: json object, html page 
"""
@login_required
def menu_home(request):
    items = Item.objects.all() #put all food items in database in this single variable
    cats = category.objects.all()

    context = {'itms':items, 'categories':cats}


    return render(request, 'menu.html',context) 

"""Overview: Renders category menu items to the user
    Return: json object, html page 
"""
@login_required
def cat_g(request, category_id):        #gives all menu items a category
    categories= category.objects.filter(pk=category_id).first()
    cats = category.objects.all()
    category_posts = Item.objects.filter(cat=categories)
    return render(request, 'menu.html', {'cats': cats,'categories':categories,'category_posts':category_posts})


    #return 0

"""Overview: Renders more details about menu item to user
    Return: json object, html page 
"""
@login_required

def item_view(request, item_id):
    item = Item.objects.filter(pk=item_id)[0] #QUERY DATABSE FOR ARGUMENT IN URL
    return render(request, 'menu_item_details.html', {'item':item})