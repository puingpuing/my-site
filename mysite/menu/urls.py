from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notice', views.notice_view, name='notice'),
    path('notice/noticewrite', views.noticewrite, name='noticewrite'),
    path('notice/postcreate', views.postcreate, name='postcreate'),
    path('notice/details/<int:pk>/', views.notice_details, name='details'),
    path('notice/details/<int:pk>/comment', views.Noticomm.as_view(), name="noticomment"),
    path('notice/details/<int:pk>/recomment', views.Notirecomm.as_view(), name="recomment"),
    path('rules', views.Rulesview.as_view(), name='rules'),
    path('rules/ruleswrite', views.Test.as_view(), name='ruleswrite'),
    path('rules/rulescreate', views.Testt.as_view(), name='rulescreate'),
    path('rules/details/<int:pk>/', views.rules_details, name='rulesdetails'),
    path('talk', views.talk, name='talk'),
    path('diary', views.diary, name='diary'),
    path('woe', views.woe, name='woe'),
    #path('findaccount/',views.findaccount, name ='findaccount'),
    #path('<int:id_text>/main/', views.main, name = 'main'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
