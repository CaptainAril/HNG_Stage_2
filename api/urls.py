from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import OrganisationDetailView, OrganisationView, UserView

urlpatterns = [
    path('token/',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('organisations', OrganisationView.as_view(), name='organisations'),
    path('organisations/<uuid:orgId>', OrganisationDetailView.as_view(), name='org_details'),
    path('organisations/<uuid:orgId>/users', OrganisationDetailView.as_view(), name='add_user'),
    
    path('users/<uuid:userId>', UserView.as_view(), name='users'),

    
]