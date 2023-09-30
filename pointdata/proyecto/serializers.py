from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'  # Incluye todos los campos del modelo
        extra_kwargs = {
            'correo': {'required': False},
            'contraseña': {'required': False},
            'nombre': {'required': False},
            'apellido': {'required': False},
            'password': {'required': False},
        }

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'

class RelevoSerializer(serializers.ModelSerializer):

    imagen = serializers.ImageField(required=False) 
   
    class Meta:
        model = Relevo
        fields = '__all__'  # Incluye todos los campos del modelo

    def validate(self, data):

        implementado = data.get('implementado')
        estado = data.get('estado')

        # Verifica las condiciones requeridas
        if implementado == 'MERCADERISMO':
            if estado != 'EFECTIVO':
                raise serializers.ValidationError("Si implementado es 'MERCADERISMO', el estado debe ser 'EFECTIVO'.")
        elif implementado == 'SIN MERCADERISMO':
            if estado not in ['CERRADO', 'NO DESEA']:
                raise serializers.ValidationError("Si implementado es 'SIN MERCADERISMO', el estado debe ser 'CERRADO' o 'NO DESEA'.")

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser
        return token