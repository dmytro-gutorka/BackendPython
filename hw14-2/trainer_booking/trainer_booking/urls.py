from django.urls import path, include

urlpatterns = [
    path('trainer/', include('trainer.urls')),
    path('booking/', include('booking.urls')),
    path('', include('user.urls')),

]