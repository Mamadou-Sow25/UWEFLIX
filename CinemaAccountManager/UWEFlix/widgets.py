from UWEFlix.models import Showing,  User
#
class ListWidget():
    # On creation
    def __init__(self, title, items):
        #
        self.title = title
        #
        self.items = items
        #
        self.type = "list"

#
class ButtonWidget():
    # On creation
    def __init__(self, title, buttons, hrefs):
        #
        self.title = title
        #
        self.buttons = []
        #
        for i, text in enumerate(buttons):
            #
            self.buttons.append(Button(text, hrefs[i]))
        #
        self.type = "button"

#
class Button():
    # On creation
    def __init__(self, text, href):
        #
        self.text = text
        #
        self.href = href

#
def getWidgets(group):
    #
    widgets = []
    #
    if group == "Cinema Manager" or group == "Cinema Employee" or group == "Admin":
        #
        showings = Showing.objects.order_by('date').order_by('time')[:10]
        #
       
        widgets.append(ListWidget("Upcoming Showings", [f"{i.film.title} in Screen {i.screen.number} at {i.date}, {str(i.time)[:5]}" for i in showings]))
        #
        widgets.append(ButtonWidget("Quick Actions", ["Add Film", "Add Showing", "Add Screen", "Add Club"], ["add_film", "log_showing", "log_screens", "add_club"]))
        #
        widgets.append(ListWidget("",""))
    
    return widgets