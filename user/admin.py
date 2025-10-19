from django.contrib import admin
from user.models import CustomUser

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')


admin.site.register(CustomUser, UserAdmin)
