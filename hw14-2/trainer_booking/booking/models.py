from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TrainerDescription(models.Model):
    trainer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    description = models.TextField()

    def __str__(self):
        return self.trainer.username


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=50, choices=[('novice', 'Novice'), ('medium', 'Medium'), ('advanced', 'Advanced')])
    duration = models.DurationField()

    def __str__(self):
        return f"{self.category.name} - {self.trainer.username}"


class TrainerSchedule(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()

    def __str__(self):
        return f"{self.trainer.username}: {self.datetime_start} - {self.datetime_end}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Booking by {self.user.username} with {self.trainer.username}"


class Rating(models.Model):
    rate = models.IntegerField()
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')

    def __str__(self):
        return f"Rating by {self.author.username} for {self.recipient.username}"