"""
URL configuration for the application.

This module defines all the paths used in the web interface, linking URLs
to their corresponding views. It includes pages for login/logout, home,
database tables (observatories, telescopes, instruments, etc.), and data download.

All pages except login/logout require authentication.
"""

# Third-party libraries
#from django.contrib.auth import views as auth_views  # to reset password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# Local application imports
from .views import *

urlpatterns = [
    # Home page - requires login
    path('home/', home_view, name='home'),

    # Login and logout pages using Django's built-in views
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Reset password
    # It was working correctly in July 2025 - currently disabled but code kept for future use
    # The code is retained in case it is decided to enable it in the future.
    # path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Database overview page - requires login
    path('database/', login_required(database_view), name='database'),

    # Pages showing lists or details of different database tables, all requiring login:
    path('groups/', login_required(groups_view), name='groups'),
    path('observatories/', login_required(observatories_view), name='observatories'),
    path('observatory/<str:observatory_name>/', login_required(observatory_view), name='observatory'),
    path('telescopes/', login_required(telescopes_view), name='telescopes'),
    path('telescope/<str:telescope_name>/', login_required(telescope_view), name='telescope'),
    path('instruments/', login_required(instruments_view), name='instruments'),
    path('researchers/', login_required(researchers_view), name='researchers'),
    path('observing_runs/', login_required(observing_runs_view), name='observing_runs'),
    path('observing_run/<str:observing_run_name>/', login_required(observing_run_view), name='observing_run'),
    path('observing_blocks/', login_required(observing_blocks_view), name='observing_blocks'),
    path('target/', login_required(targets_view), name='targets'),

    # File download for a specific target - requires login
    path('download_files/<int:target_id>/', login_required(download_files_view), name='download_files_view'),

]
