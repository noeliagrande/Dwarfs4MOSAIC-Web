"""
Middleware to safely handle session interruptions.
If a session expires, the user is notified and redirected to the login page.
"""

# Third-party libraries
from django.contrib import messages
from django.contrib.sessions.exceptions import SessionInterrupted
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import redirect

# Custom middleware that extends Django's SessionMiddleware
class SafeSessionMiddleware(SessionMiddleware):
    # Handle exceptions raised during the request
    def process_exception(self, request, exception):
        # If the session was interrupted, notify the user and redirect to login page
        if isinstance(exception, SessionInterrupted):
            messages.warning(request, "Your session has expired. Please log in again.")
            return redirect('/admin/login/')
        # For all other exceptions, let Django handle them normally
        return None