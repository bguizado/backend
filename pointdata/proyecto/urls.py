from django.urls import path
from .views import registrar, TiendasController, MyTokenObtainPairView , UsuarioController , UsuariosController
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('registro', registrar),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('tienda', TiendasController.as_view()),
    path('usuarios/', UsuariosController.as_view(), name='detalle-usuario'),
    path('usuarios/<int:id>/', UsuarioController.as_view(), name='detalle-usuario')
]
