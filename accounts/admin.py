from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import messages

class CustomUserAdmin(UserAdmin):
    actions = ['make_superuser', 'remove_superuser']

    def make_superuser(self, request, queryset):
        updated = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, f'{updated} pengguna telah dijadikan superuser dan staff.', messages.SUCCESS)
    make_superuser.short_description = "Jadikan pengguna terpilih sebagai superuser dan staff"

    def remove_superuser(self, request, queryset):
        updated = queryset.update(is_superuser=False)
        self.message_user(request, f'Status superuser telah dihapus dari {updated} pengguna.', messages.SUCCESS)
    remove_superuser.short_description = "Hapus status superuser dari pengguna terpilih"

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
