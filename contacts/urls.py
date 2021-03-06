from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls.conf import path, include
from django.views.generic.base import RedirectView

from .admin_site import contact_admin
from .views import HomeView, AdministrationView


app_name = 'contacts'

urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),
    path('admin/', admin.site.urls),
    path('admin/', contact_admin.urls),
    
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),

    path('admin/contacts/', RedirectView.as_view(url='admin/contacts/'),
         name='contacts_models_url'),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='search_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)