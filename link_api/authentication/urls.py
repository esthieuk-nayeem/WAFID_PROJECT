from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('registeradmin/', RegisterAdminView.as_view(), name="register_admin"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('userupdate/', UserVarifyView.as_view(), name="uservarify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="uservarify"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

]