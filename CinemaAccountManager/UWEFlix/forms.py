from dataclasses import fields
from django import forms
from UWEFlix.models import Film,Club, Showing, Screens,ClubRepresentative
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError

# Date widget for declaring input types within form
class DateInput(forms.DateInput):
    input_type = 'date'

# A form to add a film to the database
class LogFilmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LogFilmForm, self).__init__(*args, **kwargs)
        self.fields['duration'].widget.attrs['min'] = 0
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Film
        # Define the fields to be included in the film
        fields = ("title", "short_description", "duration", "image_URL")

# A form to add Club Details to the database
class AddClubForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Club
        # Define the fields to be included in the film
        fields = ("name", "representative", "address", "landline", "mobile")
        
# A form to add a showings to the database
class LogShowingForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Showing
        # Define the fields to be included in the film
        fields = ('date', 'time', 'film', 'taken_tickets', 'screen')
        widgets = { "date": DateInput() }
    
        
# A form to add screen to the database
class LogScreenForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Screens
        # Define the fields to be included in the film
        fields = ('capacity', 'number')

# A form to add a user to the database
class LogUserForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = User
        # Define the fields to be included in the film
        fields = ("username", "email")


class CreateUserForm(UserCreationForm):
    # metadata
    class Meta:
        # Using User models
        model = User
        # Get the username, email, password and checking password
        fields = ['username', 'email', 'password1', 'password2']

# A form to login the user
class LoginUserForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Using the User models
        model = User
        # Get the username and password
        fields = ['username', 'password']
        # Set the password as a password input to hide the text
        widgets = {'password': forms.PasswordInput()}

#
class UpdateAccountForm(forms.ModelForm):
    # metadata
    class Meta:
        # Using User models
        model = User
        # Get the username, email, password and checking password
        fields = ['username', 'email']





# A form to add a film to the database
class LogClubRepresentativeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(LogClubRepresentativeForm, self).__init__(*args, **kwargs)
    #     self.fields['mobile'].widget.attrs['max'] = 11
    # Metadata class
    class Meta:
        # Set the model type to film
        model = ClubRepresentative
        # Define the fields to be included in the film
        fields = ("firstName", "lastName", "dateOfBirth","email", "mobile")
        widgets = { "dateOfBirth": DateInput() }