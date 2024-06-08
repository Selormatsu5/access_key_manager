from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AccessKey

class CustomUserAdmin(UserAdmin):
    # Display these fields in the list view of the admin
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    # Make these fields searchable
    search_fields = ('email', 'username')
    # Specify the ordering
    ordering = ('email',)
    # Fields to display in the detail view (form view)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'other_names')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Type', {'fields': ('user_type',)}),  # Custom field added to fieldset
    )
    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

# Register your CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)

# Register AccessKey model
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'status', 'expiry_date')
    search_fields = ('user__email', 'key')
    list_filter = ('status',)

admin.site.register(AccessKey, AccessKeyAdmin)
