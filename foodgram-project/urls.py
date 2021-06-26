from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # регистрация и авторизация
    path('auth/', include('users.urls')),
    # если нужного шаблона для /auth не нашлось в файле users.urls —
    # ищем совпадения в файле django.contrib.auth.urls
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('', include('prod_h.urls')),
    path('about-author/', include('django.contrib.flatpages.urls')),
    path('about-tech/', include('django.contrib.flatpages.urls')),
]

handler404 = 'prod_h.views.page_not_found'
handler500 = 'prod_h.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
