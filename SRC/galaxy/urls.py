from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('observatory/', views.observatory, name='observatory'),
    path('telescope/', views.telescope, name='telescope'),
    path('instrument/', views.instrument, name='instrument'),
]