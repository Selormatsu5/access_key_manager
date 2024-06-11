from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import CustomUserCreationForm, AccessKeyForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import AccessKey, CustomUser
from .utils import generate_random_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
# from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been confirmed.')
        return redirect('confirmation_page')
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('login')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('keys/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
            the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def ConfirmationPage(request):
    return render(request, 'keys/confirmation_page.html')


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'keys/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        return render(request, 'keys/signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'keys/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('redirect_dashboard')
        return render(request, 'keys/login.html', {'form': form})

@login_required
def redirect_dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect(reverse('admin_dashboard'))  # Redirect to admin dashboard URL name
    elif user.groups.filter(name='IT Personnel').exists():
        return redirect(reverse('it_dashboard'))  # Redirect to IT dashboard URL name
    else:
        return redirect(reverse('login'))  # Or another default page



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
        return render(request, 'keys/admin_dashboard.html', context)

    def post(self, request):
        if 'revoke_key' in request.POST:
            key_id = request.POST.get('key_id')
            access_key = get_object_or_404(AccessKey, id=key_id)
            access_key.status = 'revoked'
            access_key.save()
            messages.success(request, 'Key has been revoked.')
        return redirect('admin_dashboard')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_it_personnel), name='dispatch')
class ITDashboardView(View):
    def get(self, request):
        user = request.user
        active_key = AccessKey.objects.filter(user=user, status='active').first()
        previous_keys = AccessKey.objects.filter(user=user).exclude(status='active')

        context = {
            'active_key': active_key,
            'previous_keys': previous_keys,
            'has_active_key': active_key is not None
        }
        return render(request, 'keys/it_dashboard.html', context)

    def post(self, request):
        if 'generate_key' in request.POST:
            user = request.user
            if AccessKey.objects.filter(user=user, status='active').exists():
                messages.error(request, 'You already have an active key.')
            else:
                key = generate_random_string()
                expiry_date = timezone.now() + timedelta(days=30)  # Key valid for 30 days
                AccessKey.objects.create(
                    user=user,
                    key=key,
                    status='active',
                    expiry_date=expiry_date
                )
                messages.success(request, 'New access key generated successfully.')
        return redirect('it_dashboard')


@method_decorator(login_required, name='dispatch')
class RevokeKeyView(View):
    def post(self, request, key_id):
        if request.user.user_type == 'Admin':
            access_key = get_object_or_404(AccessKey, id=key_id)
            access_key.status = 'revoked'
            access_key.save()
            messages.success(request, 'Key has been revoked.')
        return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'keys/profile.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'keys/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'keys/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'keys/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'keys/password_reset_complete.html'
