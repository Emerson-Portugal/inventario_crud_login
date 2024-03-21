
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('apps.login.urls', namespace='login')),
    path('inventario/', include('apps.inventario.urls', namespace='inventario')),
    path('accounts/', include('django.contrib.auth.urls')),
]