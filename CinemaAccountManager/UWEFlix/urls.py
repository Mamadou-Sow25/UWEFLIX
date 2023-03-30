from django.urls import path, include
from UWEFlix import views
from django.contrib import admin
from UWEFlix.models import Film
from django.contrib.auth import views as auth_views

# Establish the URLs
urlpatterns = [
    path("", views.home_view, name="home"),
    path("cinema_manager_home/", views.widgetHome, name="cinema_manager_home"),
    path("cinema_employee_home/", views.widgetHome, name="cinema_employee_home"),
    
    
    path("film_management/", views.film_management_view, name="film_management"),
    path("club_management/", views.club_management_view, name="club_management"),
   
    path("representative/", views.representative_view, name="represent"),
    path("about/", views.about, name="about"), 

    # Account 
    
    path('accounts/', include('django.contrib.auth.urls')),
   # path("login/", views.loginView, name="login"),
    path("accounts/login/", views.loginView, name="login_redirect"),
    path("logout/", views.userLogout, name="logout"),
   
    
    path("accesss_denied/", views.noAccess, name="no_access"),
    
    



    path("add_film/", views.log_film, name="add_film"),
    path("update_film/<str:filmName>", views.updateFilm, name="update_film"),
    path("remove_film/<str:object>", views.removeFilm, name="remove_film"),
    
    #Added paths for club rep CRUD
    path("add_clubRepresentative/", views.log_clubRepresentative, name="add_clubRepresentative"),
    path("update_clubRepresentative/<str:object>", views.updateClubRepresentative, name="update_clubRepresentative"),
    path("remove_clubRepresentative/<str:object>", views.removeClubRepresentative, name="remove_clubRepresentative"),
    path("clubRepresentative_management/", views.clubRepresentative_management_view, name="clubRepresentative_management"),
    ##############################

    path("add_club/", views.log_club, name="add_club"),
    path("update_club/<str:clubName>", views.updateClub, name="update_club"),
    path("remove_club/<str:object>", views.removeClub, name="remove_club"),
    
       
    #Screens
    path("screen/", views.screen_view, name="screens"), 
    path("log_screens/", views.log_screens, name="log_screens"), 
    path("updateScreens/<str:object>", views.updateScreens, name="updateScreens"), 
    path("removeScreens/<str:object>", views.removeScreens, name="removeScreens"), 
    
    #Showing
    path("showing/", views.showing_view, name="showing"),
    path("addShowing/", views.log_showing, name="log_showing"), 
    path("updateShowing/<str:object>", views.updateShowings, name="updateShowings"), 
    path("removeShowings/<str:object>", views.removeShowings, name="removeShowings"), 
    
   

   

    path("error/", views.error, name="error")
]   