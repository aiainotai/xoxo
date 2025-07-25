
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from ooxx import views as frnview
from xadmin import views as bendview

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('xadmin', bendview.admindash, name="xadmin" ),
    path('', frnview.index, name='index'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)