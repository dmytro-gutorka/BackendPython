from django.urls import path
from .views import *

urlpatterns = [
	path('home', home, name='home'),
	path('<booking_id>/cancel', booking_cancel, name='booking_cancel'),
	path('<booking_id>/accept', booking_accept, name='booking_accept'),
	path('<booking_id>/', booking_detail, name='booking_detail'),

]

