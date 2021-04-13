from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Customer
from games.models import childMode

def games_home(request):
    return render(request, 'Games_Page.html') #view for games home page

def games_home_guest(request):
    return render(request, 'Games_Page_Guest.html') #view for games page when not logged in

def games_home_locked(request):
    return render(request, 'Games_Page_Locked.html') #view for games home page if child mode is activated 

def games_snake(request):
    return render(request, 'snake.html') #view for snake

def games_snake_locked(request):
    return render(request, 'snake_locked.html') #view for snake if child mode is activated

def games_ttt(request):
    return render(request, 'tictactoe.html') #view for tic tac toe

def games_ttt_locked(request):
    return render(request, 'tictactoe_locked.html') #view for tic tac toe if child mode is activated

#@login_required                         #login required, cannot set a child mode lock without being logged in
def set_childmode(request):
    if request.method == "POST":                #once a passcode is submitted
        field1 = request.POST.get('att1')          #store the submitted passcodes from both fields
        field2 = request.POST.get('att2')
        currentUser = get_object_or_404(Customer, user=request.user) #get current user
        if (checkValid(field1, field2, request) == 1):              #check to make sure the passcode is valid
            pcode = childMode(passcode=field1, customer=currentUser)
            pcode.save()                                               #once passcode is valid, save and redirect to the locked game page
            return render(request, 'Games_Page_Locked.html')
        elif (checkValid(field1, field2, request) == 2):
            return render(request, 'Child_Mode_MatchError.html')
        else:
            return render(request, 'Child_Mode_Invalid.html')      
    return render(request, 'Child_Mode.html') #views for child mode

def childmode_invalid(request):                         #views for invalid child mode passcode attempts
    return render(request, 'Child_Mode_Invalid.html')
    
def childmode_matcherror(request):
    return render(request, 'Child_Mode_MatchError.html')

def deactivate_child(request):                          #view for page to deactivate child mode
    if request.method == "POST":
        currentUser = get_object_or_404(Customer, user=request.user)        #get current user logged in
        childMode_obj = get_object_or_404(childMode, customer=currentUser)  #grab the childmode object for the current user
        passcode = childMode_obj.passcode                                      #store the passcode from the childmode object
        attempt = request.POST.get('attempt')                                   #store the passcode entered by the user to check if it is right
        if (checkPass(attempt, passcode) == 1):
            childMode_obj.delete()                                              #if passcode is right, delete it and then redirect to unlocked games page
            return render(request, 'Games_Page.html')
        else:
            return render(request, 'Child_Mode_Deactivate_I.html')
    return render(request, 'Child_Mode_Deactivate.html')

def deactivate_child_error(request):                                            #view for if passcode entered is incorrect
    return render(request, 'Child_Mode_Deactivate_I.html')

def checkValid(field1, field2, request):                                        #function that checks if the passcode is 4 characters, and if both fields match
    if(field1 == field2):
        if(len(field1) == 4):
            return 1
        else:
            return 3
    else:
        return 2

def checkPass(attempt, passcode):                                               #function that checks if the entered passcode matches the stored passcode
    if(attempt == passcode):
        return 1
    else:
        return 2


