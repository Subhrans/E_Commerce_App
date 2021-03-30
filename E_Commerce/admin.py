from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Product, HomeBanner, UserProfile,Cart,Category


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'total_quantity', 'alternative_text']


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'alternative_text']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'pk']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key','expire_date']
    search_fields = ['session_key']
admin.site.register(Session,SessionAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','id']
    list_display_links = ['name','id']