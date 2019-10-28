from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('login.urls')),
    path('action/', include('useractions.urls')),
	path('', include('main.urls'))
]
