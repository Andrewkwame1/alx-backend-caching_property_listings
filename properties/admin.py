from django.contrib import admin

# Register your models here.
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'location', 'price', 'created_at')
	search_fields = ('title', 'location')
	list_filter = ('location',)
