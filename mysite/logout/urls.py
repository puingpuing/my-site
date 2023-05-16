from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.trylogout, name='logout'),
    #path('findaccount/',views.findaccount, name ='findaccount'),
    #path('<int:id_text>/main/', views.main, name = 'main'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)