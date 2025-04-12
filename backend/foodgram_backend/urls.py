from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from api.views import redirect_to_recipe
from core.constants import PREFIX_SHORT_LINK_RECIPE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(
        fr'{PREFIX_SHORT_LINK_RECIPE}(?P<short_link>[a-zA-Z0-9-]+)/',
        redirect_to_recipe
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
