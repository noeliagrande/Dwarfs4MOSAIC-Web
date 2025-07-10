from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Home page
    path('home/', home_view, name='home'),

    # Login/logout
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Download folder
    #path('download/<str:filename>/', views.download_file, name='download_file'),

    # Database page
    path('database/', login_required(database_view), name='database'),

    # 'Observatories table' page.
    path('observatories/', login_required(observatories_view), name='observatories'),

    # Page with information about a specific observatory
    path('observatory/<str:observatory_name>/', login_required(observatory_view), name='observatory'),

    # 'Telescopes table' page.
    path('telescopes/', login_required(telescopes_view), name='telescopes'),

    # Page with information about a specific telescope
    path('telescope/<str:telescope_name>/', login_required(telescope_view), name='telescope'),

    # 'Instruments table' page.
    path('instruments/', login_required(instruments_view), name='instruments'),

    # 'Researchers table' page.
    path('researchers/', login_required(researchers_view), name='researchers'),

    # 'Observing_run table' page.
    path('observing_runs/', login_required(observing_runs_view), name='observing_runs'),

    # Page with information about a specific observing_run
    path('observing_run/<str:observing_run_name>/', login_required(observing_run_view), name='observing_run'),

    # 'Observing_block table' page.
    path('observing_blocks/', login_required(observing_blocks_view), name='observing_blocks'),

    # 'Target table' page.
    path('target/', login_required(targets_view), name='targets'),

    # Files download page
    path('download_files/<int:target_id>/', login_required(download_files_view), name='download_files_view'),

]
