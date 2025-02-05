from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serve the SPA home page
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    # Include API endpoints from the members app
    path('members/', include('members.urls')),
]
