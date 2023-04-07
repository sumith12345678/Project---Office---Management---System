from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('register/<int:role>', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', Dashboard,name='dashboard'),
    path('departmentList', DepartmentList, name='departmentList'),
    path('departmentAdd', DepartmentAdd, name='departmentAdd'),
    path('departmentDelete/<int:id>',DeptDelete,name='departmentDelete'),
    path('base', base, name='base'),
    
    path('composeMessage', composeMessageView, name='composeMessage'),
    path('inbox', inboxMessageView, name='inbox'),
    path('messageDelete/<int:id>', messageDeleteView, name='messageDelete'),
    
    path('notification/', notification_add_view, name='notification_add'),
    path('news_delete/<int:id>/', notification_delete_view, name='notification_delete'),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)