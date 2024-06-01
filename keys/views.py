from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, AccessKeyForm
from .models import AccessKey, CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Create your views here.

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'keys/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
                return redirect('dashboard')
        return render(request, 'keys/login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user = request.user
        if user.user_type == 'IT':
            access_keys = AccessKey.objects.filter(user=user)
        elif user.user_type == 'Admin':
            access_keys = AccessKey.objects.all()
        context = {
            'access_keys': access_keys,
            'active_keys_count': access_keys.filter(status='active').count(),
            'expired_keys_count': access_keys.filter(status='expired').count(),
            'revoked_keys_count': access_keys.filter(status='revoked').count(),
        }
        return render(request, 'keys/dashboard.html', context)


class RevokeKeyView(View):
    def post(self, request, key_id):
        if request.user.user_type == 'Admin':
            access_key = AccessKey.objects.get(id=key_id)
            access_key.status = 'revoked'
            access_key.save()
        return redirect('dashboard')


class KeyDetailsView(View):
    def get(self, request, email):
        try:
            user = CustomUser.objects.get(email=email)
            access_key = AccessKey.objects.get(user=user, status='active')
            data = {
                'status': access_key.status,
                'date_of_procurement': access_key.date_of_procurement,
                'expiry_date': access_key.expiry_date,
            }
            return JsonResponse(data, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except AccessKey.DoesNotExist:
            return JsonResponse({'error': 'No active key found'}, status=404)
