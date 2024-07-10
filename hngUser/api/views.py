from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Organisation, User
from .permissions import isOwner
from .serializers import (LoginSerializer, OrganisationSerializer,
                          RegisterUserSerializer, UserSerializer)

# Create your views here.


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        # retrieves user detail
        try:
            user = User.objects.get(userId=userId)
            if user:
                serializer = UserSerializer(user)
                return_data = {
                    "status": "success",
                    "message": "User Data Retrieved",
                    "data": serializer.data
                }

                return Response(data=return_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={
                "status": "Bad request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)


class OrganisationView(generics.ListCreateAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Organisation.objects.filter(Q(owner=user) | Q(users=user)).distinct()

    def get(self, request, *args, **kwargs):
        try:
            orgList = super().get(request, *args, **kwargs).data
            return_data = {
                "status": "success",
                "message": f"{request.user.firstName}'s Organisations",
                "data": {
                    "organisations": orgList
                }
            }
            return Response(data=return_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.serializer_class(
                context={"owner": request.user})
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response(data={
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)


class OrganisationDetailView(APIView):

    def get_permissions(self):
        # Apply different permissions based on the action
        if self.request.method in ['POST']:
            permission_classes = [IsAuthenticated, isOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, orgId):
        # retrieves user detail
        try:
            org = Organisation.objects.get(orgId=orgId)
            if org:
                serializer = OrganisationSerializer(org)
                return_data = {
                    "status": "success",
                    "message": "Organisation Data Retrieved",
                    "data": serializer.data
                }

                return Response(data=return_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={
                "status": "Bad request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, orgId):
        try:
            org = Organisation.objects.get(orgId=orgId)
            user = User.objects.get(userId=request.data.get('userId'))
            if org:
                org.users.add(user)
                return_data = {
                    "status": "success",
                    "message": "User added to organisation successfully",
                }
                return Response(data=return_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={
                "status": "Bad request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user = authenticate(email=user['email'], password=user['password'])
            refresh = RefreshToken.for_user(user)

            org = Organisation.objects.create(
                **{"owner": user, "name": f"{user.firstName}'s Organisaton"})
            org.save()

            data = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data={
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "errors": serializer.errors,
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # login user
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.data
            user = authenticate(email=user['email'], password=user['password'])
            if user:
                login(request=request, user=user)
                refresh = RefreshToken.for_user(user)

                data = {
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "accessToken": str(refresh.access_token),
                        "user": UserSerializer(user).data
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={"status": "Bad request", "message": "Authentication failed", "errors": serializer.errors, "statusCode": 401},
                        status=status.HTTP_401_UNAUTHORIZED)


@requires_csrf_token
def custom_404(request, exception=None):
    return JsonResponse(data={"error": "Invalid Enpoint!"}, status=status.HTTP_404_NOT_FOUND)


@requires_csrf_token
def custom_405(request, exception=None):
    return JsonResponse(data={"error": "Invalid Enpoint!"}, status=status.HTTP_404_NOT_FOUND)
