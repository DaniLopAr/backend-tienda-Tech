"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView as token, TokenRefreshView as token_refresh
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def crear_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'dj02lopeza@gmail.com', 'Admin1234!')
        return HttpResponse('Superusuario creado')
    return HttpResponse('Ya existe')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('productos.urls')),
    path('api/', include('usuarios.urls')),
    path('api/ordenes/', include('ordenes.urls')),
    path('crear-admin/', crear_admin),


    # Autentitacion con JWT
    path('api/token/', token.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh.as_view(), name='token_refresh'),
]
