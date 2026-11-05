from rest_framework import serializers
from .models import Habitacion


class HabitacionSerializer(serializers.ModelSerializer):
    numero = serializers.IntegerField(min_value=1, max_value=2147483647)
    tipo = serializers.CharField(min_length=3, max_length=30, trim_whitespace=True)
    precio = serializers.IntegerField(min_value=1, max_value=9999999)

    class Meta:
        model = Habitacion
        fields = ["id", "numero", "tipo", "precio", "disponible"]
        read_only_fields = ["id"]

    def validate_numero(self, value):
        qs = Habitacion.objects.filter(numero=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe una habitación con ese número.")
        return value

    def validate_tipo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El tipo de habitación es obligatorio.")
        return value.strip()
