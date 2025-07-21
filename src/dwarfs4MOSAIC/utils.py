"""
Utility functions for handling database queries and file operations.

This module includes:
- A helper to convert raw SQL query results into dictionaries.
- File management tools for listing files, ensuring unique filenames,
  and sanitizing filenames for safe usage across platforms.
"""

# Standard libraries
import os
import re
import unicodedata

# Third-party libraries
from django.conf import settings

# Convert all rows from a DB cursor into a list of dictionaries.
# Each dictionary represents a row with column names as keys.
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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

# Generate a unique filename by adding a numeric suffix if needed.
# Example: file.txt → file (1).txt → file (2).txt, etc.
def get_unique_filename(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1

    return new_filename

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