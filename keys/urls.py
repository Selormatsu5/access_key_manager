from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
                    SignUpView, LoginView, OTPVerificationView,
                    RevokeKeyView, PasswordResetRequestView,  
                    PasswordResetOTPVerificationView, 
                    PasswordResetFormView,
                    CustomPasswordResetCompleteView, 
                    ITProfileView,
                    AdminProfileView, 
                    ConfirmationPage,
                    AdminCustomPasswordChangeView,
                    ITCustomPasswordChangeView,
                    # ActiveKeyDetailView,
                    )

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='login'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify_otp'),
    path('redirect_ dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('it-dashboard/', views.ITDashboardView.as_view(), name='it_dashboard'),
    path('myprofile/', ITProfileView.as_view(), name='myprofile'),
    path('myprofile/reset-password/', ITCustomPasswordChangeView.as_view(), name='reset_password'),
    path('profile/', AdminProfileView.as_view(), name='profile'),
    path('profile/change-password/', AdminCustomPasswordChangeView.as_view(), name='change_password'),
    path('revoke/<int:key_id>/', RevokeKeyView.as_view(), name='revoke_key'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-otp/', PasswordResetOTPVerificationView.as_view(), name='password_reset_otp'),
    path('password-reset-form/', PasswordResetFormView.as_view(), name='password_reset_form'),
    path('confirmation/', ConfirmationPage, name='confirmation_page'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('api/active-key/', ActiveKeyDetailView.as_view(), name='active_key_detail'),

]
