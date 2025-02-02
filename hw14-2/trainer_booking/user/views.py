from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages


def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f"Welcome, {username}!")
				return redirect("booking.home")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Error")
	else:
		form = AuthenticationForm()

	return render(request, "login.html", {"form": form})


def user_register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "You're now registered!")
			return redirect("booking.home")
		else:
			messages.error(request, "Error")
	else:
		form = UserCreationForm()

	return render(request, "register.html", {"form": form})


def user_logout(request):
	logout(request)
	messages.success(request, "You're now logged out!")
	return redirect("login")


def user_profile(request, user_id):
	return render(request, "profile.html")
