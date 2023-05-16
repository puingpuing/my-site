from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signform', views.signform, name="signform"),
    path('findaccount/',views.findaccount, name ='findaccount'),
    path('main/', views.main, name = 'main'),
    path('tmp/', views.tmp, name = 'tmp'),
    path('create', views.create, name = 'create'),
    path('activate/<str:uid>/<str:token>', views.activate, name = 'activate'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
