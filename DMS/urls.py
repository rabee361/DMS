"""
URL configuration for DMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import DashboardView

urlpatterns = [
    path('dms/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dms/supersecureadmin/', admin.site.urls),
    path('dms/admin/', include('fake_admin.urls')),  # Fake admin page
    path('dms/secureadmin/', include('fake_admin.urls')),  # Fake admin page
    path('dms/users/', include('users.urls')),
    path('dms/documents/', include('documents.urls')),
    path('dms/tasks/', include('tasks.urls')),
    path('dms/hr/', include('hr_tool.urls')),
    path('dms/form-builder/', include('form_builder.urls')),
    path('dms/stats/', include('stats.urls')),
    # path('error/' , )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
