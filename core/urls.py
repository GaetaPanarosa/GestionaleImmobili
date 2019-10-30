from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from core import views
from core.views import Immobili_vendita, Immobili_gestione, Immobili_affitto, Rubrica

urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.view_vendita, name="index"),
    path('logout/', views.logout, name='logout'),
    path('immobili/', views.view_vendita, name="gestione_immobili"),
    path('rubrica/', views.view_rubrica, name="gestione_rubrica"),
    path('amministrazione', views.amministrazione, name="amministrazione"),
    path('form_immobile', views.aggiungi_immobile, name="form_immobile"),
    path('immobili/modifica_immobile/<int:pk>/', views.modifica_immmobile, name="modifica_immobile"),
    path('immobili/cancella_immobile/<int:pk>/', views.cancella_immobile, name="immobile/cancella_immobile"),
    path('aggiungi_cliente', views.aggiungi_cliente, name="aggiungi_cliente"),
    path('aggiungi_cliente_immobile/', views.aggiungi_cliente_immobile, name="aggiungi_cliente_immobile"),
    path('rubrica/modifica_cliente/<int:pk>', views.modifica_cliente, name="modifica_cliente"),
    path('rubrica/cancella_cliente/<int:pk>', views.cancella_cliente, name="cancella_cliente"),
    ######################################################################################################
    url(r'^gestione_immobili_vendita/$', Immobili_vendita.as_view(), name='immobili_vendita'),
    url(r'^gestione_immobili_affitto/$', Immobili_affitto.as_view(), name='immobili_affitto'),
    url(r'^gestione_immobili_gestione/$', Immobili_gestione.as_view(), name='immobili_gestione'),
    url(r'^gestione_rubrica_clienti/$', Rubrica.as_view(), name='rubrica_clienti'),
]