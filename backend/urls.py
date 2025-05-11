
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from checklist_app.views import List, ListItems, Login, Register, Home, Logout
from drf_spectacular.views import (    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.credentials),
    path('register/', Register.register_user, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('home/', Home.dashboard, name='home'),
    path('logout/', Logout.logout, name='logout'),
    path('list/', List.list, name='new_list'),
    path('listItems/', ListItems.manage_list_items, name='list_manage'),
    path('listItems/<str:username>/<int:list_id>/', ListItems.listItems, name='list_get'),
# API Schema URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),]
