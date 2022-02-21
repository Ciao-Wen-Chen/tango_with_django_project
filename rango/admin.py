from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

#Chapter 6
# customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

#Chaper 5
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Register your models here.
# admin.site.register(Category)
# Chapter 6: replace the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)