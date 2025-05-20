from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Restaurant, Table, Reservation
from django.urls import reverse
from datetime import date, time


class BookingTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

        # Создаем ресторан и столик
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Street',
            lat=43.238949,  # Обязательное поле
            lon=76.889709  # Обязательное поле
        )
        self.table = Table.objects.create(restaurant=self.restaurant, number=1, seats=4)

    def test_user_registration(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'new@user.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # редирект после регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        login = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login)

    def test_reservation_creation(self):
        self.client.login(username='testuser', password='testpass')
        reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            date=date.today(),
            time=time(18, 0),
            guests=2
        )
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation.table, self.table)

    def test_restaurant_list_view(self):
        response = self.client.get('/restaurants/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')

    def test_reservation_requires_login(self):
        response = self.client.get(reverse('reserve') + f'?restaurant={self.restaurant.id}')
        self.assertEqual(response.status_code, 302)  # редирект на login
        self.assertIn('/accounts/login/', response.url)

    def test_invalid_reservation_form(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('reserve'), {
            'restaurant': self.restaurant.id,
            'guests': '',   # пропущено
            'date': '',
            'time': '',
        })
        self.assertContains(response, "Проверьте данные формы", status_code=200)
