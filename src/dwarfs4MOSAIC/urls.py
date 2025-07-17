"""
URL configuration for the application.

This module defines all the paths used in the web interface, linking URLs
to their corresponding views. It includes pages for login/logout, home,
database tables (observatories, telescopes, instruments, etc.), and data download.

All pages except login/logout require authentication.
"""

from django.urls import path
# from django.contrib.auth import views as auth_views # to reset password
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Home page (requires login)
    path('home/', home_view, name='home'),

    # Login / Logout (use built-in Django views)
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Reset password
    # It was working correctly in July 2025, but the feature was disabled.
    # The code is retained in case it is decided to enable it in the future.
    # path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Database summary page
    path('database/', login_required(database_view), name='database'),

    # Observatories list
    path('observatories/', login_required(observatories_view), name='observatories'),

    # Single observatory detail page
    path('observatory/<str:observatory_name>/', login_required(observatory_view), name='observatory'),

    # Telescopes list
    path('telescopes/', login_required(telescopes_view), name='telescopes'),

    # Single telescope detail page
    path('telescope/<str:telescope_name>/', login_required(telescope_view), name='telescope'),

    # Instruments list
    path('instruments/', login_required(instruments_view), name='instruments'),

    # Researchers list
    path('researchers/', login_required(researchers_view), name='researchers'),

    # Observing runs list
    path('observing_runs/', login_required(observing_runs_view), name='observing_runs'),

    # Single observing run detail page
    path('observing_run/<str:observing_run_name>/', login_required(observing_run_view), name='observing_run'),

    # Observing blocks list
    path('observing_blocks/', login_required(observing_blocks_view), name='observing_blocks'),

    # Targets list
    path('target/', login_required(targets_view), name='targets'),

    # File download view for a specific target
    path('download_files/<int:target_id>/', login_required(download_files_view), name='download_files_view'),

    # Files deletion for a specific target
    path('delete_files/<int:target_id>/', login_required(delete_files_view), name='delete_files_view'),

]
