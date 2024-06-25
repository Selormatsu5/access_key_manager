from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordChangeView
)
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import (
    CustomUserCreationForm,
    OTPVerificationForm, 
    PasswordResetRequestForm, 
    OTPVerificationForm, 
    CustomSetPasswordForm, 
    CustomPasswordChangeForm,
)
from .models import AccessKey, CustomUser, OTP
from .utils import generate_otp, send_otp_via_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
# from django.utils import timezone
from django.contrib.auth import get_user_model 


User = get_user_model()
# This OTP verification is for user registration
class OTPVerificationView(View):
    def get(self, request):
        form = OTPVerificationForm()
        messages.info(request, 'Please check your email for the OTP.')
        return render(request, 'keys/verify_otp.html', {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            otp_record = OTP.objects.filter(user=user, otp_code=otp_code, is_used=False).first()

            if otp_record and not otp_record.is_expired():
                otp_record.is_used = True
                otp_record.save()
                user.is_active = True
                user.save()
                login(request, user)
                # messages.success(request, 'Your account has been activated successfully.')
                return redirect('confirmation_page')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        return render(request, 'keys/verify_otp.html', {'form': form})

def ConfirmationPage(request):
    return render(request, 'keys/confirmation_page.html')


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'keys/split_signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp_code = generate_otp(user)
            send_otp_via_email(user,otp_code)
            
            request.session['user_id'] = user.id  # Store user ID in session for OTP verification
            return redirect('verify_otp')
        else:
            messages.error(request, 'Error in registration form. Please try again.')
        return render(request, 'keys/split_signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'keys/split_login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                # Directly call the function to redirect based on group
                return redirect_dashboard(request)
        # If form is invalid, re-render login page with form
        return render(request, 'keys/split_login.html', {'form': form})


@login_required
def redirect_dashboard(request):
    user = request.user
    print(f"Redirecting user: {user.email}, Groups: {user.groups.all()}")

    if user.groups.filter(name='Admin').exists():
        print("Redirecting to Admin Dashboard")
        return redirect(reverse('admin_dashboard'))  # Redirect to admin dashboard URL name
    elif user.groups.filter(name='IT Personnel').exists():
        print("Redirecting to IT Dashboard")
        return redirect(reverse('it_dashboard'))  # Redirect to IT dashboard URL name
    else:
        print("No matching group, redirecting to login")
        return redirect(reverse('login'))


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_it_personnel(user):
    return user.groups.filter(name='IT Personnel').exists()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        it_users = CustomUser.objects.filter(user_type='IT')
        it_keys = {user: AccessKey.objects.filter(user=user) for user in it_users}

        context = {
            'it_users': it_users,
            'it_keys': it_keys
        }
        return render(request, 'keys/admin/admin_dashboard.html', context)

    def post(self, request):
        if 'revoke_key' in request.POST:
            key_id = request.POST.get('key_id')
            access_key = get_object_or_404(AccessKey, id=key_id)
            access_key.revoke()
            messages.success(request, 'Key has been revoked.')
        return redirect('admin_dashboard')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_it_personnel), name='dispatch')
class ITDashboardView(View):
    def get(self, request):
        user = request.user
        active_key = AccessKey.objects.filter(user=user, status='active').first()
        expired_keys = AccessKey.objects.filter(user=user, status='expired')
        revoked_keys = AccessKey.objects.filter(user=user, status='revoked')

        context = {
            'active_key': active_key,
            'expired_keys': expired_keys,
            'revoked_keys': revoked_keys,
            'has_active_key': active_key is not None
        }
        return render(request, 'keys/it/it_dashboard.html', context)

    def post(self, request):
        if 'generate_key' in request.POST:
            user = request.user
            try:
                AccessKey.create_key(user)
                messages.success(request, 'New access key generated successfully.')
            except ValueError as e:
                messages.error(request, str(e))
        return redirect('it_dashboard')


@method_decorator(login_required, name='dispatch')
class RevokeKeyView(View):
    def post(self, request, key_id):
        if request.user.user_type == 'Admin':
            access_key = get_object_or_404(AccessKey, id=key_id)
            access_key.revoke()
            messages.success(request, 'Key has been revoked.')
        return redirect('admin_dashboard')


@method_decorator(login_required, name='dispatch')
class ITProfileView(View):
    def get(self, request):
        return render(request, 'keys/it/profile.html')


@method_decorator(login_required, name='dispatch')
class AdminProfileView(View):
    def get(self, request):
        return render(request, 'keys/admin/profile.html')
    
class AdminCustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'keys/admin/change_password.html'
    success_url = reverse_lazy('profile')  # User would be redirected to profile after successful password change

    def form_valid(self, form):
        # Save the new password and update the user's session
        user = form.save()
        update_session_auth_hash(self.request, user)  # This would keep the user logged in
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ITCustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'keys/it/reset_password.html'
    success_url = reverse_lazy('myprofile')  # Redirect to profile after successful password change

    def form_valid(self, form):
        # Save the new password and update the user's session
        user = form.save()
        update_session_auth_hash(self.request, user)  # Important to keep the user logged in
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'keys/password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            
            # Generate or update the OTP for the user
            otp_code = generate_otp(user)

            # Send the OTP via email
            send_otp_via_email(user, otp_code)

            
            request.session['reset_user_id'] = user.id
            return redirect(reverse('password_reset_otp'))
        return render(request, 'keys/password_reset_request.html', {'form': form})



class PasswordResetOTPVerificationView(View):
    def get(self, request):
        form = OTPVerificationForm()
        return render(request, 'keys/otp_verification.html', {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user_id = request.session.get('reset_user_id')

            if user_id:
                user = get_object_or_404(User, pk=user_id)
                otp_record = OTP.objects.filter(user=user, otp_code=otp_code, is_used=False).first()

                if otp_record and not otp_record.is_expired():
                    otp_record.is_used = True
                    otp_record.save()

                    messages.success(request, 'OTP verified. You can now reset your password.')
                    request.session['otp_verified_user_id'] = user_id
                    return redirect('password_reset_form')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
            else:
                messages.error(request, 'Session expired. Please request a new password reset.')
                return redirect('password_reset_request')

        return render(request, 'keys/otp_verification.html', {'form': form})


class PasswordResetFormView(View):
    def get(self, request):
        form = CustomSetPasswordForm(user=request.user)
        return render(request, 'keys/password_reset_form.html', {'form': form})

    def post(self, request):
        user_id = request.session.get('otp_verified_user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            form = CustomSetPasswordForm(user=user, data=request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Please correct the errors below.')

        else:
            messages.error(request, 'Session expired. Please request a new password reset.')
            return redirect('password_reset_request')

        return render(request, 'keys/password_reset_form.html', {'form': form})


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'keys/password_reset_complete.html'