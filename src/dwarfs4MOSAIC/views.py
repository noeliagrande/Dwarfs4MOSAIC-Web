"""
Views for the dwarfs4MOSAIC web interface.

This module provides page rendering and logic for:
- Viewing all tables (targets, observatories, telescopes, etc.)
- Navigating between related entities
- Downloading data files (individually or as ZIP)
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .utils import get_files, get_unique_filename, sanitize_filename

import os
from django.conf import settings
from django.contrib import messages

from django.http import FileResponse

import zipfile
import tempfile

# Home page showing all targets and associated files (if authenticated)
def home_view(request):
    context = {}
    if request.user.is_authenticated:
        # Prefetch related data to reduce database queries:
        if request.user.is_superuser or request.user.researcher.role == "core_team":
            # 'admin' and 'core team' have permission to see everything
            lst_targets = Tbl_target.objects.prefetch_related('observing_blocks__obs_run__instrument').distinct()
        else:
            # 'collaborator' users has permission to see only authorized blocks
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
            # Get associated files if 'datafiles_path' is defined
            files = get_files(target.datafiles_path) if target.datafiles_path else []

            # Deduplicate observing runs
            seen_runs = set() # Set to track already added obs_run
            unique_runs = []  # Final list of unique obs_run objects

            for block in target.observing_blocks.all():
                run = block.obs_run
                key = str(run)
                if key not in seen_runs:
                    seen_runs.add(key)
                    unique_runs.append(run)

            # Deduplicate instruments
            seen_instruments = set()  # Set to track already added instruments
            unique_instruments = []   # Final list of unique instrument objects
            for run in unique_runs:
                instr = run.instrument
                key = str(instr)
                if key not in seen_instruments:
                    seen_instruments.add(key)
                    unique_instruments.append(instr)

            # Add everything to the rendering context
            lst_targets_and_files.append({
                'target': target,
                'files': files,
                'unique_obs_runs': unique_runs,
                'unique_instruments': unique_instruments,
            })

        context['authenticated'] = True
        context['lst_targets_and_files'] = lst_targets_and_files
    else:
        context['authenticated'] = False

    return render(request, 'dwarfs4MOSAIC/home.html', context)

# Static database overview page
def database_view(request):
    return render(request, 'dwarfs4MOSAIC/database.html')

# Page listing all groups
def groups_view(request):
    lst_groups = Group.objects.exclude(name='admin').order_by("name")

    return render(request, 'dwarfs4MOSAIC/groups.html', {
        'lst_groups': lst_groups
    })

# Page listing all observatories
def observatories_view(request):
    lst_observatories = Tbl_observatory.objects.all().order_by("name")

    return render(request, 'dwarfs4MOSAIC/observatories.html', {
        'lst_observatories': lst_observatories
    })

# Page listing all telescopes of a specific observatory
def observatory_view(request, observatory_name):
    observatory = get_object_or_404(Tbl_observatory, name = observatory_name) # Get observatory by name
    telescopes = Tbl_telescope.objects.filter(obs_tel = observatory) # Get telescopes belonging to the observatory

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory_name': observatory_name,
        'lst_telescopes': telescopes
    })

# Page listing all telescopes
def telescopes_view(request):
    lst_telescopes = Tbl_telescope.objects.all().select_related("obs_tel").order_by("name")

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {
        'lst_telescopes': lst_telescopes
    })

# Page listing all instruments of a specific telescope
def telescope_view(request, telescope_name):
    telescope = get_object_or_404(Tbl_telescope, name = telescope_name) # Get telescope by name
    instruments = Tbl_instrument.objects.filter(tel_ins = telescope) # Get instruments belonging to the telescope

    return render(request, 'dwarfs4MOSAIC/telescope.html', {
        'telescope': telescope,
        'lst_instruments': instruments
    })

# Page listing all instruments
def instruments_view(request):
    lst_instruments = Tbl_instrument.objects.all().select_related("tel_ins").order_by("name")

    return render(request, 'dwarfs4MOSAIC/instruments.html', {
        'lst_instruments': lst_instruments
    })

# Page listing all researchers
def researchers_view(request):
    lst_researchers = Tbl_researcher.objects.all()

    return render(request, 'dwarfs4MOSAIC/researchers.html', {
        'lst_researchers': lst_researchers
    })

# Page listing all observing runs
def observing_runs_view(request):
    lst_observing_runs = Tbl_observing_run.objects.all().select_related('instrument')

    return render(request, 'dwarfs4MOSAIC/observing_runs.html', {
        'lst_observing_runs': lst_observing_runs
    })

# Page showing a specific observing run with its blocks and researchers
def observing_run_view(request, observing_run_name):
    observing_run = get_object_or_404(Tbl_observing_run, name = observing_run_name) # Get observing_run by name
    observing_blocks = Tbl_observing_block.objects.filter(obs_run = observing_run.id) # Get observing_blocks belonging to the observing_run
    researchers = observing_run.researchers.all() # Get researchers participating in the observing_run

    return render(request, 'dwarfs4MOSAIC/observing_run.html', {
        'observing_run': observing_run,
        'lst_observing_blocks': observing_blocks,
        'lst_researchers': researchers})

# Page listing all observing blocks
def observing_blocks_view(request):
    lst_observing_blocks = Tbl_observing_block.objects.all().select_related('obs_run').prefetch_related('target')

    return render(request, 'dwarfs4MOSAIC/observing_blocks.html', {
        'lst_observing_blocks': lst_observing_blocks})

# Page listing all targets
def targets_view(request):
    lst_targets = Tbl_target.objects.all()

    return render(request, 'dwarfs4MOSAIC/targets.html', {
        'lst_targets': lst_targets})

# Allow the user to download one or multiple data files associated with a target.
# - If one file is selected, it is served directly.
# - If multiple files are selected, they are compressed into a ZIP archive.
def download_files_view(request, target_id):
    target = get_object_or_404(Tbl_target, pk=target_id)
    files = get_files(target.datafiles_path) if target.datafiles_path else []

    if request.method == "POST":
        selected_files = request.POST.getlist('checkbox_single[]')
        source_dir = os.path.join(settings.MEDIA_ROOT, target.datafiles_path)

        # Send a single file
        if len(selected_files) == 1:
            filename = os.path.basename(selected_files[0])
            filepath = os.path.join(source_dir, sanitize_filename(filename))
            if not os.path.exists(filepath):
                messages.error(request, "File not found.")
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)

        # If more than one file, create a ZIP archive of multiple files
        tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        with zipfile.ZipFile(tmp_zip.name, 'w') as zipf:
            for fname in selected_files:
                safe_name = os.path.basename(fname)
                full_path = os.path.join(source_dir, safe_name)
                if os.path.exists(full_path):
                    zipf.write(full_path, arcname=safe_name)  # arcname = no internal path
                else:
                    print(f"File not found: {safe_name}")  # Optional: log or warning

        # Custom download filename
        if hasattr(target, 'name'):
            safe_name = sanitize_filename(target.name)
            zip_filename = f"{safe_name}_files.zip"
        else:
            zip_filename = "files.zip"

        return FileResponse(open(tmp_zip.name, 'rb'), as_attachment=True, filename=zip_filename)

    return render(request, 'dwarfs4MOSAIC/download_files.html', {
        'target': target,
        'lst_files': files,
        'select_all_tooltip': 'Click to choose all files at once',
        'btn_download_tooltip': 'Download selected files',
    })