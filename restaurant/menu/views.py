from django.shortcuts import render

# Create your views here.

"""Overview: Render the menu page to the user
    Return: Returns a render response to the client 
"""
def menu_home(request):
    return render(request, 'menu.html')

