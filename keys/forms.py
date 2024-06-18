from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import CustomUser, AccessKey

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        
        fields = ('first_name', 'other_names','username','email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = AccessKey
        fields = ['status', 'expiry_date']

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, required=True, label='OTP Code')

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, label='Email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with this email address.")
        return email
        
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

