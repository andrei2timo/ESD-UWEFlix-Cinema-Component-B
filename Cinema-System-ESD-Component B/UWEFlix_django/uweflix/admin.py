from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

# Register your models here.

# The register() method is called on the Django admin site object admin.site to register 
# the models for use in the admin interface.
# In this case, the User, Film, Customer, ClubRep, Showing, and Screen models are all being registered.
# The second argument passed to the register() method is the custom admin class that will be used for the corresponding model in the admin interface. 
# In the case of the User model, the custom admin class is CustomUserAdmin, which is defined earlier in the code.
# By registering these models with their corresponding admin classes, the Django admin site will use the customizations provided by the admin classes when displaying and editing data for these models in the admin interface.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Film)
admin.site.register(Customer)
admin.site.register(ClubRep)
admin.site.register(Showing)
admin.site.register(Screen)