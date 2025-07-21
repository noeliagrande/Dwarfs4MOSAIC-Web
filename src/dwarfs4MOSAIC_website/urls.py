"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Third-party libraries
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#from django.contrib.auth import views as auth_views  # to change/reset password
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('', include('dwarfs4MOSAIC.urls')),

    # Change password (user logged)
    # It was working correctly in July 2025, but the feature was disabled.
    # The code is retained in case it is decided to enable it in the future.
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Reset password (user unlogged)
    # It was working correctly in July 2025, but the feature was disabled.
    # The code is retained in case it is decided to enable it in the future.
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) # Configured to serve the media files
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
