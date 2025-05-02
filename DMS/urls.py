from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import DashboardView, FormView
from django.views.generic import TemplateView

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
    path('dms/404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('dms/500/', TemplateView.as_view(template_name='500.html'), name='500'),
    path('dms/form/<slug:slug>/', FormView.as_view(), name='form'),
    path('dms/api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
