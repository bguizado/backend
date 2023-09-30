from django.urls import path
from .views import registrar, TiendasController, MyTokenObtainPairView, TiendaController
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('registro', registrar),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('tienda/<id>', TiendaController.as_view()),
    path('tiendas', TiendasController.as_view())
]
