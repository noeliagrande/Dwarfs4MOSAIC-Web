"""
Utility functions for handling database queries and file operations.

This module includes:
- A helper to convert raw SQL query results into dictionaries.
- File management tools for listing files, ensuring unique filenames,
  and sanitizing filenames for safe usage across platforms.
"""

import os
import shutil
from django.conf import settings
import unicodedata
import re

# Return all rows from a database cursor as a list of dictionaries.
# Each dictionary corresponds to a row, with column names as keys.
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Return a list of files inside the directory specified by the relative media path.
# Args:
#     path (str): Relative path from MEDIA_ROOT to the target directory.
# Returns:
#     list: List of filenames if the directory exists, otherwise an empty list.
def get_files(path):
    if not path:
        return []

    full_path = os.path.join(settings.MEDIA_ROOT, path)

    try:
        files = os.listdir(full_path)
        return files
    except FileNotFoundError:
        return []

# Add a numeric suffix to the filename if it already exists in the destination directory.
# Prevents overwriting existing files by creating unique variants like:
# 'file.txt' → 'file (1).txt', 'file (2).txt', etc.
# Args:
#     dest_dir (str): Destination directory.
#     filename (str): Desired filename.
# Returns:
#     str: A unique filename within the destination directory.
def get_unique_filename(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1

    return new_filename

# Convert a filename to a safe, ASCII-only format.
# - Removes accents and special characters.
# - Keeps only alphanumeric characters, dashes, underscores, periods, and spaces.
# - Replaces spaces with underscores.
# Args:
#     name (str): Original filename or string.
# Returns:
#     str: Sanitized filename.
def sanitize_filename(name):
    # Normalize Unicode characters (e.g., é → e, ñ → n)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

    # Remove invalid characters
    name = re.sub(r'[^\w\-. ]', '', name)

    # Replace spaces with underscores
    name = name.replace(' ', '_')

    return name