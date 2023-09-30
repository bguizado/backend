from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *
from .models import *
from boto3 import session
from os import environ, path
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
        method='post',
        operation_description="Envia el registro de la tienda"
)

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
    #se agrego swagger_auto_schema para la documentacion ,probar
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='ID del usuario', type=openapi.TYPE_STRING)
        ],
    )

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
        serializador = RelevoSerializer(data=request.data)
        if serializador.is_valid():
            nuevoRelevo = Relevo(**serializador.validated_data)
            nuevoRelevo.save()

            if nuevoRelevo.imagen:
                print(settings.BASE_DIR)
                subir_imagen_s3('{}/media/{}'.format(settings.BASE_DIR, nuevoRelevo.imagen))

            return Response(data={'message': 'Relevo creado exitosamente'}, status=status.HTTP_201_CREATED)
        else: 
            return Response(data={'message': 'No se pudo crear el relevo',
                              'content': serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        relevos = Relevo.objects.all()
        serializador = RelevoSerializer(relevos, many=True)

        return Response(data={
            'message': 'Relevos: ',
            'content': serializador.data
        }, status=status.HTTP_200_OK)

def subir_imagen_s3(nombre_imagen):
    if nombre_imagen is None:
        return
    
    nuevaSesion = session.Session(
            aws_access_key_id=environ.get('AWS_ACCESS_KEY'), 
            aws_secret_access_key=environ.get('AWS_SECRET_KEY'), 
            region_name=environ.get('AWS_BUCKET_REGION'))
    
    s3Client = nuevaSesion.client('s3')

    bucket = environ.get('AWS_BUCKET_NAME')
    with open(nombre_imagen, 'rb') as archivo:
        object_name = path.basename(archivo.name)
        print(object_name)
        try:
            respuesta = s3Client.upload_file(nombre_imagen, bucket, object_name)
            print(respuesta)
        except Exception as e:
            print(e)