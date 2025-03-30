from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Home page
    path('home/', views.home_view, name='home'),

    # Login/logout
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Database page
    path('database/', views.database_view, name='database'),

    # 'Observatories table' page.
    path('observatories/', views.observatories_view, name='observatories'),

    # Page with information about a specific observatory
    path('observatory/<str:observatory_name>/', views.observatory_view, name='observatory'),

    # 'Telescopes table' page.
    path('telescopes/', views.telescopes_view, name='telescopes'),

    # Page with information about a specific telescope
    path('telescope/<str:telescope_name>/', views.telescope_view, name='telescope'),

    # 'Instruments table' page.
    path('instruments/', views.instruments_view, name='instruments'),

    # Page with information about a specific instrument
    path('instrument/<str:instrument_name>/', views.instrument_view, name='instrument'),

    # 'Researchers table' page.
    path('researchers/', views.researchers_view, name='researchers'),

    # 'Observing_run table' page.
    path('observing_runs/', views.observing_runs_view, name='observing_runs'),

    # Page with information about a specific observing_run
    path('observing_run/<str:observing_run_name>/', views.observing_run_view, name='observing_run'),

    # 'Observing_block table' page.
    path('observing_blocks/', views.observing_blocks_view, name='observing_blocks'),

    # 'Target table' page.
    path('target/', views.targets_view, name='targets'),
]
