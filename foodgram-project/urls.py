from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # ссылки на кастомные страницы ошибок
    path('500/', views.server_error, name='500'),
    path('404/', views.page_not_found, name='404'),
    # регистрация и авторизация
    path('auth/', include('users.urls')),
    # если нужного шаблона для /auth не нашлось в файле users.urls —
    # ищем совпадения в файле django.contrib.auth.urls
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('', include('prod_h.urls')),
    # ссылки на информацию о сайте
    path('about-author/', include('django.contrib.flatpages.urls')),
    path('about-tech/', include('django.contrib.flatpages.urls')),
]

handler404 = 'foodgram-project.views.page_not_found'
handler500 = 'foodgram-project.views.server_error'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
