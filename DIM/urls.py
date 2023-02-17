from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('school.urls', 'school'), namespace='school')),
    path('auth/', include(('authentication.urls', 'authentication'), namespace='auth')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('basket/', include(('basket.urls', 'basket'), namespace='basket')),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

