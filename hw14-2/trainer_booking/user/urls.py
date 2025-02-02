from django.urls import path
from .views import *

urlpatterns = [
	path('login/', user_login, name='login'),
	path('registration/', user_register, name='registration'),
	path('logout/', user_logout, name='logout'),
	path('user/<int:user_id>', user_profile, name='profile'),
]
