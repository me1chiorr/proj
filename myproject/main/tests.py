from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta

from .models import Restaurant, Table, Reservation

User = get_user_model()

class ReservationFormTests(TestCase):
    def setUp(self):
        # Создаём пользователя и объекты для брони
        self.user = User.objects.create_user(username='test', password='pass')
        self.restaurant = Restaurant.objects.create(
            name='Testaurant', address='Test Address'
        )
        self.table = Table.objects.create(
            restaurant=self.restaurant, number=1, seats=4
        )

    def test_cannot_book_past_date(self):
        """Форма не пропустит бронь на вчера."""
        from .forms import ReservationForm

        data = {
            'table': self.table.id,
            'date': date.today() - timedelta(days=1),
            'time': time(12, 0),
        }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Нельзя бронировать на прошедшую дату.', form.non_field_errors()
        )

    def test_cannot_double_book(self):
        """Нельзя забронировать один и тот же стол на одинаковую дату/время."""
        # сначала создаём бронь напрямую
        Reservation.objects.create(
            user=self.user, table=self.table,
            date=date.today() + timedelta(days=1),
            time=time(13, 0)
        )
        from .forms import ReservationForm

        data = {
            'table': self.table.id,
            'date': date.today() + timedelta(days=1),
            'time': time(13, 0),
        }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'уже забронирован', form.non_field_errors()[0]
        )

class ReservationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.reserve_url = reverse('reserve')
        self.login_url   = reverse('login')

    def test_anonymous_redirects_to_login(self):
        """Аноним при GET /reserve/ уходит на страницу логина."""
        resp = self.client.get(self.reserve_url)
        self.assertRedirects(
            resp,
            f"{self.login_url}?next={self.reserve_url}"
        )

    def test_logged_in_can_access_reserve(self):
        """Залогиненный видит страницу брони."""
        user = User.objects.create_user('u', password='p')
        self.client.login(username='u', password='p')
        resp = self.client.get(self.reserve_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<form')

class APIReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('apiuser', password='p')
        self.restaurant = Restaurant.objects.create(
            name='API R', address='API Addr'
        )
        self.table = Table.objects.create(
            restaurant=self.restaurant, number=5, seats=2
        )

    def test_api_requires_authentication(self):
        """Без логина API /api/reservations/ возвращает 401."""
        resp = self.client.get('/api/reservations/')
        self.assertEqual(resp.status_code, 401)

    def test_api_list_and_create(self):
        """После логина можно получить список и создать бронь."""
        self.client.login(username='apiuser', password='p')
        # GET
        resp = self.client.get('/api/reservations/')
        self.assertEqual(resp.status_code, 200)
        # POST
        data = {
            'table': self.table.id,
            'date': (date.today() + timedelta(days=2)).isoformat(),
            'time': time(14, 0).isoformat(),
        }
        resp = self.client.post('/api/reservations/', data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Reservation.objects.count(), 1)
