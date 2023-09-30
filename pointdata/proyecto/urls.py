from django.urls import path
from .views import registrar, TiendasController, TiendaController, MyTokenObtainPairView , UsuarioController , UsuariosController, RelevoController
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('registro', registrar),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('tienda/<id>', TiendaController.as_view()),
    path('tiendas', TiendasController.as_view()),
    path('tienda', TiendasController.as_view()),
    path('usuarios/', UsuariosController.as_view(), name='detalle-usuario'),
    path('usuarios/<int:id>/', UsuarioController.as_view(), name='detalle-usuario'),
    path('relevo/', RelevoController.as_view(), name='relevo')
]
