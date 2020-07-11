from .models import Profile

from django.contrib import admin

# Register your models here.
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['']
admin.site.register(Profile)