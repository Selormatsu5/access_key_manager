from django.urls import path
from .views import SignUpView, LoginView, DashboardView, RevokeKeyView, KeyDetailsView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('revoke/<int:key_id>/', RevokeKeyView.as_view(), name='revoke_key'),
    path('api/key-details/<str:email>/', KeyDetailsView.as_view(), name='key_details'),
]
