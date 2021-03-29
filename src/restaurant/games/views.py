from django.shortcuts import render

def games_home(request):
    return render(request, 'Games_Page.html') #view for games home page

def games_snake(request):
    return render(request, 'snake.html') #view for snake

def games_ttt(request):
    return render(request, 'tictactoe.html') #view for tic tac toe

def set_childmode(request):
    return render(request, 'Child_Mode.html') #views for child mode

def deactivate_child(request):
    return render(request, 'Child_Mode_Deactivate.html') 
