from django.urls import path, include
from booking.views import *

urlpatterns = [
    path('trainer/', include('trainer.urls')),
    path('booking/', include('booking.urls')),
    path('/', include('user.urls')),

]