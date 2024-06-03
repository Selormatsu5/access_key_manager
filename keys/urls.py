from django.urls import path

from .views import SignUpView, LoginView, DashboardView, RevokeKeyView, KeyDetailsView, ProcureKeyView, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('revoke/<int:key_id>/', RevokeKeyView.as_view(), name='revoke_key'),
    path('keys/procure/', ProcureKeyView.as_view(), name='procure_key'),
    path('api/key-details/<str:email>/', KeyDetailsView.as_view(), name='key_details'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
