from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Vendor, Review
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Vendor)

@admin.register(Review)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

#mix profile info + user info
class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["user_name", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


#Unregester the old way
admin.site.unregister(User)

#register the new way
admin.site.register(User, UserAdmin)