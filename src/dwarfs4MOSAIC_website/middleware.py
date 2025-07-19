from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.exceptions import SessionInterrupted
from django.contrib import messages
from django.shortcuts import redirect

class SafeSessionMiddleware(SessionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, SessionInterrupted):
            messages.warning(request, "Your session has expired. Please log in again.")
            return redirect('/admin/login/')
        return None