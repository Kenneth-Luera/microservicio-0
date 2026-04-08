
from django.contrib import admin
from django.urls import path
from user.userApp.views import RegisterView, get_user_data, internal_user_detail, my_profile, update_profile
from rest_framework_simplejwt.views import TokenRefreshView
from user.userApp.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', RegisterView.as_view()),
    path('api/login/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/me/', get_user_data),
    path('internal/users/<uuid:user_id>/', internal_user_detail),
    path('api/profile/me/', my_profile),
    path('profile/update/', update_profile, name='update-profile'),
]
