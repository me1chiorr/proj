# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import requests

from rest_framework import generics, permissions

from .models import Restaurant, Table, Reservation
from .forms import ReservationForm, CustomUserCreationForm
from .serializers import RestaurantSerializer, ReservationSerializer
from .views_external import external_restaurants


def index(request):
    return render(request, 'main/index.html')


def home(request):
    return render(request, 'main/index.html')


def about(request):
    return HttpResponse('')


def restaurant_list(request):
    # локальные рестораны из БД
    local_restaurants = Restaurant.objects.all()
    # внешние рестораны из 2ГИС
    external = external_restaurants()

    # **ВАЖНО** — именно здесь мы **возвращаем** результат!
    return render(request, 'main/restaurant_list.html', {
        'local_restaurants':    local_restaurants,
        'external_restaurants': external,
        'dgis_api_key':         settings.DGIS_API_KEY,  # понадобится в JS-карте
    })


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'main/reservation_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


class RestaurantListAPI(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class ReservationListCreateAPI(generics.ListCreateAPIView):
    serializer_class   = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required
def my_reservations(request):
    reservations = (Reservation.objects
                    .filter(user=request.user)
                    .order_by('-date', '-time'))
    return render(request, 'main/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
    return redirect('my_reservations')
