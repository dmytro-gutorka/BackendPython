from django.urls import path
from .views import *

urlpatterns = [
	path('<id>', trainer_detail, name='trainer_detail'),
	path('<id>/<service_id>', trainer_service, name='trainer_service'),
	path('', trainer_list, name='trainer_list'),

]