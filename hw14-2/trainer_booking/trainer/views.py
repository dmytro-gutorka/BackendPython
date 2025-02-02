from django.http import HttpResponse
from django.shortcuts import render


def trainer_list(request):
	return HttpResponse("trainer_list")


def trainer_detail(request, id):
	return HttpResponse("trainer_detail")


def trainer_service(request, id):
	return HttpResponse("trainer_service")