from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, LoginView, RevokeKeyView, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, ProfileView, ConfirmationPage
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='login'),
    path('redirect_dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('it-dashboard/', views.ITDashboardView.as_view(), name='it_dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('revoke/<int:key_id>/', RevokeKeyView.as_view(), name='revoke_key'),
    # path('keys/procure/', ProcureKeyView.as_view(), name='procure_key'),
    # path('api/key-details/<str:email>/', KeyDetailsView.as_view(), name='key_details'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('confirmation/', ConfirmationPage, name='confirmation_page'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
