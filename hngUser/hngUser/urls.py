"""
URL configuration for hngUser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from api.views import LoginView, RegisterUserView, custom_404, custom_405
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

# handler404 = custom_404
# handler405 = custom_405


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterUserView.as_view(), name='register'),
    
    # path('404/', custom_404, name='custom_404'),
    # path('405/', custom_405, name='custom_405'),
]
