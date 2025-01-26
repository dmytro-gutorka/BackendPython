from .models import *
from .forms import *


class TrainerListView(View):
    def get(self, request):
        categories = Category.objects.all()
        trainers = User.objects.filter(trainer_profile__isnull=False)
        return render(request, 'trainers/trainer_list.html', {'categories': categories, 'trainers': trainers})


class TrainerDetailView(View):
    def get(self, request, trainer_id):
        trainer = get_object_or_404(User, id=trainer_id, trainer_profile__isnull=False)
        services = trainer.services.all()
        return render(request, 'trainers/trainer_detail.html', {'trainer': trainer, 'services': services})


class BookingCreateView(View):
    def get(self, request, trainer_id, service_id):
        service = get_object_or_404(Service, id=service_id, trainer_id=trainer_id)
        form = BookingForm()
        return render(request, 'booking/booking_form.html', {'form': form, 'service': service})

    def post(self, request, trainer_id, service_id):
        service = get_object_or_404(Service, id=service_id, trainer_id=trainer_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.trainer = service.trainer
            booking.status = 'pending'
            booking.save()
            return HttpResponseRedirect(reverse('booking_detail', args=[booking.id]))
        return render(request, 'booking/booking_form.html', {'form': form, 'service': service})


class BookingDetailView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        return render(request, 'booking/booking_detail.html', {'booking': booking})