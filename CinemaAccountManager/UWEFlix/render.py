from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth.models import Group

from UWEFlix.models import Film
from math import ceil

# Establish a text item object
class TextItem():
    # On creation
    def __init__(self, text):
        # Get the text
        self.text = text
        # Set the item type
        self.type = "text"

# Establish the navigation item class
class LinkItem():
    # Initiate the item
    def __init__(self, text, href):
        # Get the text
        self.text = text
        # Get the href link
        self.href = href
        # Set the item type
        self.type = "link"



# Establish the navigation bar items

login_nav_item = LinkItem("Login", 'login')

film_mgt_nav_item = LinkItem("Films", 'film_management')

clubRepresentative_mgt_nav_item = LinkItem("Club Representative", 'clubRepresentative_management')
club_mgt_nav_item = LinkItem("Clubs", 'club_management')

screen_mgt_nav_item = LinkItem("Screen", 'screens')
showing_mgt_nav_item = LinkItem("Showing", 'showing')


# Establish the header for each user type
group_nav_dictionary = {
    "None": [login_nav_item],
    "Cinema Employee": [ film_mgt_nav_item, showing_mgt_nav_item, screen_mgt_nav_item],
    "Cinema Manager": [ film_mgt_nav_item, club_mgt_nav_item, showing_mgt_nav_item, screen_mgt_nav_item,clubRepresentative_mgt_nav_item],
    "Admin": [ film_mgt_nav_item,club_mgt_nav_item,  showing_mgt_nav_item, screen_mgt_nav_item]
}

# Establish the user information items
welcome_message_user_item = TextItem("Hello, ")
logout_user_item = LinkItem("Logout", 'logout')


# Set a dictionary for the user items
user_dictionary = {
    "None": [],     
    "Cinema Employee": [welcome_message_user_item, logout_user_item],
    "Cinema Manager": [welcome_message_user_item, logout_user_item],
    "Admin": [welcome_message_user_item, logout_user_item]
}

# Get the user's group
def getGroup(user):
    # If the user doesn't belong to a group
    if len(user.groups.all()) == 0:
        # Return none
        return "None"
    # Otherwise return the user's group
    return user.groups.all()[0].name



# Overwrite the get context data function
def getFilmContext(column_number):
    # Get the films through an SQL query
    film_list = Film.objects.order_by("-upload_date")
    # Define the film list, split into rows
    split_film_list = []
    # Calculate the number of rows
    row_number = ceil(len(film_list)/column_number)
    # For each row
    for row in range(row_number):
        # Get the start position of films to get from the film list
        start_pos = row * column_number
        # Get the end position of films to get from the film list
        end_pos = start_pos + column_number
        # If the end position is beyond the size of the film list 
        if end_pos > len(film_list):
            # Set the position to the size of the film list
            end_pos = len(film_list)
        # Add a list of films for the row on to the split film list
        split_film_list.append(Film.objects.order_by("-upload_date")[start_pos:end_pos])
    # Define the movies list in the context as the split film list
    context = {'movies_list': split_film_list}
    # Return the context
    return context

# get the widgets for the user
def getWidgetContext(request):
    # Create the context
    context = {}
    # Return the context
    return context

#
def getTopBarContext(request, context = {}):
    # Get the user's group
    user_group = getGroup(request.user)
    # Get the navigation items for the user
    context["nav_items"] = group_nav_dictionary[user_group]
    # Get the user items
    context["user_items"] = user_dictionary[user_group]
    # Get the user's group
    context["user_group"] = user_group
    # If the user is logged in
    if not request.user.is_anonymous:
        # Add their name to the user item
        context["user_items"][0].text = f"Hello, {request.user.username}!"
        
    return context

# Render the page with the user's navigation items
def dynamicRender(request, page, context = {}):
    #
    context = getTopBarContext(request, context)
    # Return the render of the page
    return render(request, page, context)