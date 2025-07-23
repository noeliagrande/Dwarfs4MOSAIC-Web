"""
Views for the dwarfs4MOSAIC web interface.

This module provides page rendering and logic for:
- Viewing all tables (targets, observatories, telescopes, etc.)
- Navigating between related entities
- Downloading data files (individually or as ZIP)
"""

# Standard libraries
import os
import tempfile
import zipfile

# Third-party libraries
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import FileResponse
from django.shortcuts import render

# Local application imports
from .models import *
from .utils import get_files, get_unique_filename, sanitize_filename

# Home page showing all targets and their files for authenticated users
def home_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.researcher.role == "core_team":
            # If user is admin or core team, show all targets with related data
            lst_targets = Tbl_target.objects.prefetch_related('observing_blocks__obs_run__instrument').distinct()
        else:
            # For collaborators, filter targets by allowed groups and exclude denied blocks
            denied_blocks = request.user.researcher.denied_blocks.all()

            lst_targets = Tbl_target.objects.filter(
                observing_blocks__allowed_groups__in = request.user.groups.all()
            ).exclude(
                observing_blocks__in = denied_blocks
            ).prefetch_related(
                'observing_blocks__obs_run__instrument'
            ).distinct()

        lst_targets_and_files = []

        for target in lst_targets:
            # Get list of files for the target if datafiles_path is set
            files = get_files(target.datafiles_path) if target.datafiles_path else []

            # Remove duplicate observing runs for this target
            seen_runs = set() # Set to track already added obs_run
            unique_runs = []  # Final list of unique obs_run objects

            for block in target.observing_blocks.all():
                run = block.obs_run
                key = str(run)
                if key not in seen_runs:
                    seen_runs.add(key)
                    unique_runs.append(run)

            # Remove duplicate instruments from the unique observing runs
            seen_instruments = set()  # Set to track already added instruments
            unique_instruments = []   # Final list of unique instrument objects
            for run in unique_runs:
                instr = run.instrument
                key = str(instr)
                if key not in seen_instruments:
                    seen_instruments.add(key)
                    unique_instruments.append(instr)

            # Add target info and related data to the context list
            lst_targets_and_files.append({
                'target': target,
                'files': files,
                'unique_obs_runs': unique_runs,
                'unique_instruments': unique_instruments,
            })

        context['authenticated'] = True
        context['lst_targets_and_files'] = lst_targets_and_files
    else:
        # User not authenticated
        context['authenticated'] = False

    # Render the home page template with context
    return render(request, 'dwarfs4MOSAIC/home.html', context)

# Render static database overview page
def database_view(request):
    return render(request, 'dwarfs4MOSAIC/database.html')

# List all user groups except 'admin'
def groups_view(request):
    lst_groups = Group.objects.exclude(name='admin').order_by("name")

    return render(request, 'dwarfs4MOSAIC/groups.html', {
        'lst_groups': lst_groups
    })

# List all observatories ordered by name
def observatories_view(request):
    lst_observatories = Tbl_observatory.objects.all().order_by("name")

    return render(request, 'dwarfs4MOSAIC/observatories.html', {
        'lst_observatories': lst_observatories
    })

# Show one observatory and its telescopes
def observatory_view(request, observatory_name):
    # Try to get the observatory by name, returns None if not found
    observatory = Tbl_observatory.objects.filter(name=observatory_name).first()

    # Get telescopes for the observatory only if the observatory exists, otherwise return an empty list
    telescopes = Tbl_telescope.objects.filter(obs_tel=observatory) if observatory else []

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory_name': observatory_name,
        'lst_telescopes': telescopes
    })

# List all telescopes with related observatories
def telescopes_view(request):
    lst_telescopes = Tbl_telescope.objects.all().select_related("obs_tel").order_by("name")

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {
        'lst_telescopes': lst_telescopes
    })

# Show one telescope and its instruments
def telescope_view(request, telescope_name):
    # Try to get the telescope by name, returns None if not found
    telescope = Tbl_telescope.objects.filter(name=telescope_name).first()

    # Get instruments for the telescope only if the telescope exists, otherwise return an empty list
    instruments = Tbl_instrument.objects.filter(tel_ins=telescope) if telescope else []

    return render(request, 'dwarfs4MOSAIC/telescope.html', {
        'telescope': telescope,
        'lst_instruments': instruments
    })

# List all instruments with related telescopes
def instruments_view(request):
    lst_instruments = Tbl_instrument.objects.all().select_related("tel_ins").order_by("name")

    return render(request, 'dwarfs4MOSAIC/instruments.html', {
        'lst_instruments': lst_instruments
    })

# List all researchers
def researchers_view(request):
    lst_researchers = Tbl_researcher.objects.all()

    return render(request, 'dwarfs4MOSAIC/researchers.html', {
        'lst_researchers': lst_researchers
    })

# List all observing runs with related instruments
def observing_runs_view(request):
    lst_observing_runs = Tbl_observing_run.objects.all().select_related('instrument')

    return render(request, 'dwarfs4MOSAIC/observing_runs.html', {
        'lst_observing_runs': lst_observing_runs
    })

# Show details for one observing run, including blocks and researchers
def observing_run_view(request, observing_run_name):
    # Try to get the observing run by name, returns None if not found
    observing_run = Tbl_observing_run.objects.filter(name=observing_run_name).first()

    # Get observing blocks of the observing run only if the observing run exists, else empty list
    observing_blocks = Tbl_observing_block.objects.filter(obs_run=observing_run.id) if observing_run else []

    # Get researchers involved only if the observing run exists, else empty queryset
    researchers = observing_run.researchers.all() if observing_run else []

    return render(request, 'dwarfs4MOSAIC/observing_run.html', {
        'observing_run': observing_run,
        'lst_observing_blocks': observing_blocks,
        'lst_researchers': researchers})

# List all observing blocks with related observing runs and targets
def observing_blocks_view(request):
    lst_observing_blocks = Tbl_observing_block.objects.all().select_related('obs_run').prefetch_related('target')

    return render(request, 'dwarfs4MOSAIC/observing_blocks.html', {
        'lst_observing_blocks': lst_observing_blocks})

# List all targets
def targets_view(request):
    lst_targets = Tbl_target.objects.all()

    return render(request, 'dwarfs4MOSAIC/targets.html', {
        'lst_targets': lst_targets})

# Allow download of one or multiple files for a target
# - Single file served directly
# - Multiple files compressed into a ZIP archive
def download_files_view(request, target_id):
    # Try to get the target by primary key, returns None if not found
    target = Tbl_target.objects.filter(pk=target_id).first()

    # Get files only if target exists and has a datafiles_path, else empty list
    files = get_files(target.datafiles_path) if target and target.datafiles_path else []

    if request.method == "POST":
        selected_files = request.POST.getlist('checkbox_single[]')
        source_dir = os.path.join(settings.MEDIA_ROOT, target.datafiles_path)

        # Serve a single selected file
        if len(selected_files) == 1:
            filename = os.path.basename(selected_files[0])
            filepath = os.path.join(source_dir, sanitize_filename(filename))
            if not os.path.exists(filepath):
                messages.error(request, "File not found.")
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)

        # Create a ZIP file for multiple selected files
        tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        with zipfile.ZipFile(tmp_zip.name, 'w') as zipf:
            for fname in selected_files:
                safe_name = os.path.basename(fname)
                full_path = os.path.join(source_dir, safe_name)
                if os.path.exists(full_path):
                    zipf.write(full_path, arcname=safe_name)  # Add file without folder structure

        # Define the ZIP file name
        if hasattr(target, 'name'):
            safe_name = sanitize_filename(target.name)
            zip_filename = f"{safe_name}_files.zip"
        else:
            zip_filename = "files.zip"

        # Serve the ZIP archive for download
        return FileResponse(open(tmp_zip.name, 'rb'), as_attachment=True, filename=zip_filename)

    # Render the file selection page
    return render(request, 'dwarfs4MOSAIC/download_files.html', {
        'target': target,
        'lst_files': files,
        'select_all_tooltip': 'Click to choose all files at once',
        'btn_download_tooltip': 'Download selected files',
    })