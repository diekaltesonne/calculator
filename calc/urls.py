from django.urls import path
from . import views
app_name = 'calc'

urlpatterns = [
 path('', views.manage_storages, name='manage_storages'),
 path('coordinate_update/', views.coordinate_update, name='coordinate_update'),
]