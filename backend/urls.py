from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView
)
from checklist_app.views import List, ListItems,  Register, Home, Logout
from checklist_app.views.TokenViews import (
    EncryptedTokenObtainPairView,
    EncryptedTokenRefreshView,

)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register.register_user, name='register'),
    path('api/token/', EncryptedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', EncryptedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', Logout.logout, name='token_blacklist'),
    path('home/', Home.dashboard, name='home'),
    path('list/', List.list, name='new_list'),
    path('listItems/', ListItems.manage_list_items, name='list_manage'),
    path('listItems/<str:username>/<int:list_id>/', ListItems.listItems, name='list_get'),
# API Schema URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),]
