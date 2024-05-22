from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('insurance_register', views.insurance_register, name='insurance_register'),

    path('insurance_list/<str:username>', views.insurance_list, name='insurance_list'),

    path('decrypt/<str:username>', views.decrypt_and_view, name='decrypt_and_view'),

    path('gen_key', views.gen_key, name='gen_key'),

    path('admin_approval', views.admin_approval, name='admin_approval'),

]