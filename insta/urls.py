from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('insta/', views.display_images, name = 'display_images'),
    path('',views.instapic, name = 'instapic'),
    # path('my_ajax_view/', views.my_ajax_view, name='my_ajax_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

