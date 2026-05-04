from django.contrib import admin
from .models import CBHI

@admin.register(CBHI)
class CBHIAdmin(admin.ModelAdmin):
    # This hides the 'admin' field from the form so you don't have to see/select it
    exclude = ('admin',)

    def save_model(self, request, obj, form, change):
        # If this is a new object (not an update), assign the current logged-in user
        if not change:
            obj.admin = request.user
        
        # Save the object
        super().save_model(request, obj, form, change)