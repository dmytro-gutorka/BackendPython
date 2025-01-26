from django.urls import path

urlpatterns = [
	path('login', 'login', name='login'),
	path('registration', 'registration', name='registration'),
	path('logout', 'logout', name='logout'),
]
