from django.contrib import admin
from django.urls import path, include
# CRITICAL: You must import the view you want to use
from applications.views import landing_page 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. This handles the login/logout URLs (Fixes your 404 error)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 2. This links to your apps/urls.py file
    path('applications/', include('applications.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),

    path('create-admin/', create_admin_user),
    
    # 3. This is your homepage
    path('', landing_page, name='index'),
]
