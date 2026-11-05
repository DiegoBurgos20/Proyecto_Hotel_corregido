from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Habitacion


class HabitacionAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="prueba", password="ClaveSegura123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.room = Habitacion.objects.create(numero=101, tipo="Suite", precio=80000)

    def test_api_requiere_token(self):
        self.client.credentials()
        response = self.client.get("/api/habitaciones/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_habitaciones(self):
        response = self.client.get("/api/habitaciones/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_consultar_por_id(self):
        response = self.client.get(f"/api/habitaciones/{self.room.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["numero"], 101)

    def test_crear_habitacion(self):
        response = self.client.post("/api/habitaciones/", {
            "numero": 102, "tipo": "Doble", "precio": 45000, "disponible": True
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habitacion.objects.filter(numero=102).exists())

    def test_rechaza_datos_invalidos(self):
        response = self.client.post("/api/habitaciones/", {
            "numero": -1, "tipo": "A", "precio": 0, "disponible": True
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_habitacion(self):
        response = self.client.put(f"/api/habitaciones/{self.room.pk}/", {
            "numero": 101, "tipo": "Presidencial", "precio": 120000, "disponible": False
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.tipo, "Presidencial")

    def test_eliminar_habitacion(self):
        response = self.client.delete(f"/api/habitaciones/{self.room.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habitacion.objects.filter(pk=self.room.pk).exists())

    def test_registro_inexistente(self):
        response = self.client.get("/api/habitaciones/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_entrega_token(self):
        self.client.credentials()
        response = self.client.post("/api/token/", {
            "username": "prueba", "password": "ClaveSegura123!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
