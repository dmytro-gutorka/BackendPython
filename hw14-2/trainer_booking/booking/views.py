from django.http import HttpResponse


def home(request):
    return HttpResponse("Home page")


def booking_cancel(request, booking_id):
    return HttpResponse(f"Booking Canceled {booking_id}")


def booking_accept(request, booking_id):
    return HttpResponse(f"Booking accepted {booking_id}")


def booking_detail(request, booking_id):
    return HttpResponse(f"Booking detail {booking_id}")