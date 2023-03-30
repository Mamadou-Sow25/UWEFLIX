from datetime import datetime
from django.shortcuts import redirect

from UWEFlix.models import Film, Showing, Screens, ClubRepresentative
from UWEFlix.forms import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from django.contrib import messages
from UWEFlix.decorators import *
from email import *
from django.contrib.auth.forms import PasswordChangeForm

from UWEFlix.render import dynamicRender, getFilmContext, getGroup
import random
import string
from UWEFlix.widgets import getWidgets

from django.db.models import ProtectedError

# Student view presenting the UI to book tickets
def home_view(request):
    # Get the films
    context = getFilmContext(3)
    # Get the user group
    group = getGroup(request.user)
    # Otherwise if they are the cinema manager
    if group == "Cinema Manager":
        # Take them to the cinema manager home
        return redirect('cinema_manager_home')
    # If they are a cinema employee
    elif group == "Cinema Employee":
        # Take them to the cinema employee home
        return redirect('cinema_employee_home')
    elif request.user.is_superuser:
          return redirect(to="/admin")
    
    return dynamicRender(request, "UWEFlix/home.html", context)

# Get the home page for the user type
def widgetHome(request):
    # Get the films
    context = getFilmContext(3)
    #
    context["widgets"] = getWidgets(getGroup(request.user))
    # Return the home page
    return dynamicRender(request, "UWEFlix/widget_home.html", context)

# About page view navigated from navbar
def about(request):
    return dynamicRender(request, "UWEFlix/about.html")
# About page view navigated from navbar
def error(request):
    return dynamicRender(request, "UWEFlix/error.html")
# View to provide representative a UI to manage films
def movies(request):
    return dynamicRender(request, "UWEFlix/movies.html")


@unauthenticated_required
def loginView(request):
    
    return redirect('login')

# Logout view
def userLogout(request):
    # Log the user out
    logout(request)
    # Redirect them to the home page
    return redirect('home')



# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def film_management_view(request):
    filmList = Film.objects.all()
    return dynamicRender(request, "UWEFlix/film_manager.html",{'filmList':filmList})


# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def club_management_view(request):
    clubList = Club.objects.all()
    return dynamicRender(request, "UWEFlix/club_manager.html",{'clubList':clubList})



# View to provide representative a UI to manage films
def representative_view(request):
    return dynamicRender(request, "UWEFlix/representative.html")

# View to provide representative a UI to manage films
def noAccess(request):
    return dynamicRender(request, "UWEFlix/no_access.html")

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of films to the database
def log_film(request):

    # Define the form
    form = LogFilmForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the film is valid
        if form.is_valid():
            # Save the film details
            film = form.save(commit=False)
            film.upload_date = datetime.now()
            film.save()
            # Return the user to the homepage
            return redirect("film_management")
    # Otherwise
    else:
        # Take the user to the film creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update a film in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateFilm(request, filmName):
    film = Film.objects.get(title = filmName)
    form = LogFilmForm(instance=film)
  
    if request.method == "POST":
        # If the film is valid
        form = LogFilmForm(request.POST, instance = film)
        if form.is_valid():
           
            # Save the film details
            film = form.save(commit=False)
            film.upload_date = datetime.now()
            film.save()
            return redirect("film_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeFilm(request,object):
    film = Film.objects.get(title = object)
    if request.method == "POST":
        # Get all the showings
        showings = Showing.objects.all()
        # Is the film currently showing?
        current_showing = False
        # For each showing
        for showing in showings:
            # If the showing's film is the film to delete
            if showing.film == film:
                # Mark the film as currently showing
                current_showing = True
                # Break the loop
                break
        # If the film isn't currently showing
        if current_showing == False:
            # Delete the film from the database
            try:
                film.delete()
            except ProtectedError:
                error_message = "This object can't be deleted!!"
                return redirect('error')
        return redirect("film_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": film.title})



@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
# Function to allow the addition of clubss to the database
def log_club(request):
    # Define the form
    form = AddClubForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the club is valid
        if form.is_valid():
            # Save the club details
            club = form.save(commit=False)
            club.save()
            # Return the user to the homepage
            return redirect("club_management")
    # Otherwise
    else:
        # Take the user to the form page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})


@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateClub(request,clubName):
    club = Club.objects.get(name = clubName)
    form = AddClubForm(instance=club)
  
    if request.method == "POST":
        # If the club is valid
        form = AddClubForm(request.POST, instance = club)
        if form.is_valid():
           
            # Save the club details
            club = form.save(commit=False)
            club.save()
            return redirect("club_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeClub(request,object):
    club = Club.objects.get(name = object)
    if request.method == "POST":
        try:
            club.delete()
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return redirect('error')
        
        return redirect("club_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": club.name})






# View to allow the cinema manager to manage the users
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def user_management_view(request):
    # Get all the users
    user_list = User.objects.all()
    # Create a list to store roles
    roles = []
    # For each user
    for u in user_list:
        # Add the role
        roles.append(getGroup(u))
    # Package the users with the groups
    zipped_list = zip(user_list, roles)
    # Render the page with the users and groups
    return dynamicRender(request, "UWEFlix/user_manager.html", {'user_list': zipped_list})

# Log the user
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def log_user(request):
    # Define the form
    form = CreateUserForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the booking is valid
        if form.is_valid():
            # Save the booking details
            user = form.save(commit = False)
            user.save()
            # Set the user's group to student - the basic level account
            user.groups.add(Group.objects.get(name="Student"))
            # messages.success(request, 'Details for ' + user.username + ' created successfully!')
            # Return the user to the homepage
            return redirect("user_management")
    # Take the user to 
    return dynamicRender(request, "UWEFlix/userCRUD/form.html", {"form": form, "creating": True})




    #Showings 

def showing_view(request):
    showingList = Showing.objects.all()
    return dynamicRender(request, "UWEFlix/showings.html", {'showingList':showingList})
    
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of showings to the database
def log_showing(request):
    # Define the form
    form = LogShowingForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the showings is valid
        if form.is_valid():
            # Save the film details
            showing = form.save(commit=False)
            showing.upload_date = datetime.now()
            showing.save()
            # Return the user to the homepage
            return redirect("showing")
        else:
            return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

    return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update showings in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateShowings(request, object):
    showingName = Showing.objects.get(id = object )
    form = LogShowingForm(instance=showingName)
    if request.method == "POST":
        # If the film is valid
        form = LogShowingForm(request.POST, instance = showingName)
        if form.is_valid():
            # Save the film details
            showingName = form.save(commit=False)
            showingName.save()
            return redirect("showing")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeShowings(request,object):
    showingName = Showing.objects.get(id = object)
    if request.method == "POST":
        try:
            showingName.delete()
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return redirect('error')
        
        return redirect("showing")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": showingName.id})

#Screens 

def screen_view(request):
    screenList = Screens.objects.all()
    return dynamicRender(request, "UWEFlix/screens.html", {'screenList':screenList})
    
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of screens to the database
def log_screens(request):
    # Define the form
    form = LogScreenForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the screens is valid
        if form.is_valid():
            # Save the film details
            screens = form.save(commit=False)
            screens.save()
            # Return the user to the homepage
            return redirect("screens")
    # Otherwise
    else:
        # Take the user to the film creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update screens in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateScreens(request, object):
    screenName = Screens.objects.get(id = object )
    
    form = LogScreenForm(instance=screenName)
  
    if request.method == "POST":
        # If the film is valid
        form = LogScreenForm(request.POST, instance = screenName)
        if form.is_valid():
           
            # Save the film details
            screenName = form.save(commit=False)
            screenName.save()
            return redirect("screens")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeScreens(request,object):
    screenName = Screens.objects.get(id = object)
    if request.method == "POST":
        try:
            screenName.delete()
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return redirect('error')
        
        return redirect("screens")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": screenName.id})





# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def clubRepresentative_management_view(request):
    repList = ClubRepresentative.objects.all()
    return dynamicRender(request, "UWEFlix/clubRep_manager.html",{'clubRep_list':repList})



@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of clubReps to the database
def log_clubRepresentative(request):
    # Define the form
    form = LogClubRepresentativeForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            password = ''.join(random.choices(string.ascii_lowercase, k=10))
            clubRep = form.save(commit=False)
            clubRep.save()
            #Create a new user to allow the rep to login using their rep number and password
            clubRepUser = User(
                username = str(clubRep.clubRepNumber),
                email = clubRep.email
            )

            clubRepUser.set_password(password)
            clubRepUser.save()
            # Set the user's group to club rep
            clubRepUser.groups.add(Group.objects.get(name="Club Representative"))
            clubRep.representative = clubRepUser
            clubRep.clubRepPassword = password
            clubRep.save()
            # Return the user to the homepage
            return redirect("clubRepresentative_management")
        else:
            return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})
    # Otherwise
    else:
        # Take the user to the clubRep creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update screens in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateClubRepresentative(request, object):
    clubRep = ClubRepresentative.objects.get(clubRepNumber = object )
    
    form = LogClubRepresentativeForm(instance=clubRep)
  
    if request.method == "POST":
        # If the film is valid
        form = LogClubRepresentativeForm(request.POST, instance = clubRep)
        if form.is_valid():
           
            # Save the film details
            clubRep = form.save(commit=False)
            clubRep.save()
            return redirect("clubRepresentative_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeClubRepresentative(request,object):
    clubRep = ClubRepresentative.objects.get(clubRepNumber = object)
    user = User.objects.get(username = object)
    if request.method == "POST":
        try:
            clubRep.delete()
            user.delete()
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return redirect('error')
            
        
        return redirect("clubRepresentative_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": clubRep.clubRepNumber})

