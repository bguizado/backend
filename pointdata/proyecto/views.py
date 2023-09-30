from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail
from .serializers import *
from .models import *
from boto3 import session

@api_view(['POST'])
@permission_classes([IsAdminUser])
def registrar(request: Request):
    serializador = UsuariosSerializer(data=request.data)

    if serializador.is_valid():
        nuevoUsuario = Usuario(**serializador.validated_data)
        password = serializador.validated_data.get('password')
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()

        subject = 'Registro exitoso'
        message = f'Gracias por registrarte. Tu contraseña es: {password}'
        from_email = 'isaias.guizado@gmail.com'
        recipient_list = [nuevoUsuario.correo]
        send_mail(subject, message, from_email, recipient_list)

        return Response(data={'message': 'Usuario registrado exitosamente'},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(data={
            'message': 'Error al crear el usuario',
            'content': serializador.errors
        })


class UsuariosController(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        usuarios = Usuario.objects.all()
        serializador = UsuariosSerializer(usuarios, many=True)

        return Response(data={
            'message': 'Usuarios : ',
            'content': serializador.data
        }, status=status.HTTP_200_OK)


class UsuarioController(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request: Request, id: str):
        usuarioEncontrado = Usuario.objects.filter(id=id).first()
        if not usuarioEncontrado:
            return Response(data={
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        serializador = UsuarioSerializer(
            instance=usuarioEncontrado)
        return Response(data={
            'content': serializador.data
        }, status=status.HTTP_200_OK)

    def put(self, request: Request, id: str):
        usuarioEncontrado = Usuario.objects.filter(id=id).first()
        if not usuarioEncontrado:
            return Response(data={
                'message': 'Usuario no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializador = UsuarioSerializer(data=data)
        dataValida = serializador.is_valid()
        if dataValida:
            serializador.validated_data
            serializador.update(usuarioEncontrado, serializador.validated_data)

            return Response(data={
                'message': 'Usuario actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        else:
            return Response(data={
                'message': 'Error al actualizar el usuario',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id: str):
        usuarioEncontrado = Usuario.objects.filter(id=id).first()
        if not usuarioEncontrado:
            return Response(data={
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        Usuario.objects.filter(id=id).delete()

        return Response(data={
            'message': 'Usuario eliminado exitosamente'
        }, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TiendasController(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request: Request):
        serializador = TiendaSerializer(data=request.data)

        if serializador.is_valid():
            nuevaTienda = Tienda(**serializador.validated_data)
            nuevaTienda.save()

            return Response(data={
                'message': 'Tienda creada exitosamente'
            }, status=status.HTTP_201_CREATED)

        else:

            return Response(data={
                'message': 'Error al crear la tienda',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        tiendas = Tienda.objects.all()
        serializador = TiendaSerializer(tiendas, many=True)

        return Response(data={
            'message': 'Tiendas: ',
            'content': serializador.data
        }, status=status.HTTP_200_OK)


class TiendaController(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, id: str):
        tiendaEncontrada = Tienda.objects.filter(id=id).first()
        if not tiendaEncontrada:
            return Response(data={
                'message': 'Tienda no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        serializador = TiendaSerializer(
            instance=tiendaEncontrada)
        return Response(data={
            'content': serializador.data
        }, status=status.HTTP_200_OK)

    def put(self, request: Request, id: str):
        tiendaEncontrada = Tienda.objects.filter(id=id).first()
        if not tiendaEncontrada:
            return Response(data={
                'message': 'Tienda no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializador = TiendaSerializer(data=data)
        dataValida = serializador.is_valid()
        if dataValida:
            serializador.validated_data
            serializador.update(tiendaEncontrada, serializador.validated_data)

            return Response(data={
                'message': 'Tienda actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        else:
            return Response(data={
                'message': 'Error al actualizar la tienda',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id: str):
        tiendaEncontrada = Tienda.objects.filter(id=id).first()
        if not tiendaEncontrada:
            return Response(data={
                'message': 'Tienda no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        Tienda.objects.filter(id=id).delete()

        return Response(data={
            'message': 'Tienda eliminada exitosamente'
        }, status=status.HTTP_200_OK)


class RelevoController (APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        usuario = request.user
        request.data['usuario'] = usuario.id
        serializer = RelevoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'Relevo creado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(data={'message': 'No se pudo crear el relevo',
                              'content': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        relevos = Relevo.objects.all()
        serializador = RelevoSerializer(relevos, many=True)

        return Response(data={
            'message': 'Relevos: ',
            'content': serializador.data
        }, status=status.HTTP_200_OK)