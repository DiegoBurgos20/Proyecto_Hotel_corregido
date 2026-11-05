from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Habitacion
from .serializers import HabitacionSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_login(request):
    """Entrega un token al validar usuario y contraseña."""
    username = str(request.data.get("username", "")).strip()
    password = request.data.get("password", "")
    if not username or not password:
        return Response(
            {"error": "Debes enviar username y password."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"error": "Usuario o contraseña incorrectos."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if not user.is_active:
        return Response({"error": "La cuenta está desactivada."}, status=status.HTTP_403_FORBIDDEN)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "user": user.username, "detail": "Autenticación correcta."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_logout(request):
    request.user.auth_token.delete()
    return Response({"detail": "Sesión API cerrada correctamente."}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_habitaciones(request):
    if request.method == "GET":
        habitaciones = Habitacion.objects.all().order_by("numero")
        return Response(HabitacionSerializer(habitaciones, many=True).data)

    serializer = HabitacionSerializer(data=request.data)
    if serializer.is_valid():
        habitacion = serializer.save()
        return Response(HabitacionSerializer(habitacion).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_habitacion_detalle(request, pk):
    try:
        habitacion = Habitacion.objects.get(pk=pk)
    except Habitacion.DoesNotExist:
        return Response({"error": "La habitación no existe."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(HabitacionSerializer(habitacion).data)

    if request.method == "PUT":
        serializer = HabitacionSerializer(habitacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    habitacion.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
