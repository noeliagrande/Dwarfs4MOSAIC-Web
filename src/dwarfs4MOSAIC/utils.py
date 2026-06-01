"""
General utility module for the Django project.

Provides reusable helper functions for common backend tasks.
"""

# Standard libraries
import os
import re
import unicodedata

# Third-party libraries
from django.conf import settings


# List files inside a directory relative to MEDIA_ROOT.
# Returns a list of filenames or empty list if directory does not exist.
def get_files(path):
    if not path:
        return []

    full_path = os.path.join(settings.MEDIA_ROOT, path)

    try:
        files = os.listdir(full_path)
        return files
    except FileNotFoundError:
        return []

# Sanitize a filename by:
# - Removing accents and special Unicode characters.
# - Keeping only letters, numbers, dashes, underscores, periods, and spaces.
# - Replacing spaces with underscores.
def sanitize_filename(name):
    # Normalize Unicode characters to ASCII equivalents (e.g., é → e, ñ → n)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

    # Remove invalid characters
    name = re.sub(r'[^\w\-. ]', '', name)

    # Replace spaces with underscores
    name = name.replace(' ', '_')

    return name
