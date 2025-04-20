from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'main/index.html')

def about(request):
    return HttpResponse()


def home(request):
    return render(request, 'main/index.html')
from .models import Restaurant

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurant_list.html', {'restaurants': restaurants})


from django.shortcuts import render, redirect
from .forms import ReservationForm

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Не забудь: user должен быть залогинен
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'main/reservation_form.html', {'form': form})


from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Restaurant, Table, Reservation

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # авто-вход после регистрации
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


from rest_framework import generics, permissions
from .models import Restaurant, Table, Reservation
from .serializers import RestaurantSerializer, ReservationSerializer

class ReservationListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import generics
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantListAPI(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

from django.contrib.auth.decorators import login_required
from .models import Reservation

@login_required
def my_reservations(request):
    # вытаскиваем все брони текущего пользователя, сортируем по дате/времени
    reservations = (
        Reservation.objects
        .filter(user=request.user)
        .order_by('-date', '-time')
    )
    return render(request, 'main/my_reservations.html', {
        'reservations': reservations
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Reservation

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    # на GET можно просто редиректить или показывать подтверждение
    return redirect('my_reservations')
