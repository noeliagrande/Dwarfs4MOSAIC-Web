import os
import shutil
from django.conf import settings

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_files(path):
    if not path:
        return []

    full_path = os.path.join(settings.MEDIA_ROOT, path)

    try:
        files = os.listdir(full_path)
        return files
    except FileNotFoundError:
        return []

# Add suffix to files to avoid overwriting them
def get_unique_filename(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1

    return new_filename