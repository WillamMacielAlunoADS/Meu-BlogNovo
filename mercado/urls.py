from django.urls import path
from . import views

urlpatterns = [
    path('', views.compra_edit, name='compra_edit'),
    path('produto/', views.produto, name='produto'),
    path('cancelar_compra', views.cancelar_compra, name='cancelar_compra'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('compras_list/', views.compras_list, name='compras_list'),
    path('compra_detal/<int:pk>/', views.compra_detal, name='compra_detal'),
]