from rest_framework_simplejwt.views import TokenObtainPairView
from user.userApp.serializers import CustomTokenObtainPairSerializer
from rest_framework import generics, permissions
from user.userApp.serializers import RegisterSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_data(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def internal_user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
