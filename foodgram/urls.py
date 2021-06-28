from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # регистрация и авторизация
    path('auth/', include('users.urls')),
    # если нужного шаблона для /auth не нашлось в файле users.urls —
    # ищем совпадения в файле django.contrib.auth.urls
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # ссылки на информацию о сайте
    path('about-author/', views.AboutAuthor.as_view(), name='about_author'),
    path('about-tech/', views.AboutTech.as_view(), name='about_tech'),
    path('', include('prod_h.urls')),

]

handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
