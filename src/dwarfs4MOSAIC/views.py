from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import *
from .utils import get_files, get_unique_filename

import os
import shutil
from django.conf import settings
from django.contrib import messages

# 'Home' page.
def home_view(request):

    context = {}
    if request.user.is_authenticated:
        # Get datafiles for each target
        lst_targets = Tbl_target.objects.prefetch_related('observing_blocks__obs_run')
        lst_targets_with_files = []

        for target in lst_targets:
            # Get files only if datafiles_path has value
            if target.datafiles_path:
                files = get_files(target.datafiles_path)

                lst_targets_with_files.append({
                    'target': target,
                    'files': files
                })
            else:
                lst_targets_with_files.append({
                    'target': target,
                    'files': []
                })

        context['authenticated'] = True
        context['lst_targets_with_files'] = lst_targets_with_files
    else:
        context['authenticated'] = False

    return render(request, 'dwarfs4MOSAIC/home.html', context)

# 'Database tables' page.
def database_view(request):
    return render(request, 'dwarfs4MOSAIC/database.html')

# 'Observatories table' page.
def observatories_view(request):
    lst_observatories = Tbl_observatory.objects.all().order_by("name")

    return render(request, 'dwarfs4MOSAIC/observatories.html', {
        'lst_observatories': lst_observatories
    })

# Page with telescopes for a specific observatory
def observatory_view(request, observatory_name):
    observatory = get_object_or_404(Tbl_observatory, name = observatory_name) # Get observatory by name
    telescopes = Tbl_telescope.objects.filter(obs_tel = observatory) # Get telescopes belonging to the observatory

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory_name': observatory_name,
        'lst_telescopes': telescopes
    })

# 'Telescopes table' page.
def telescopes_view(request):
    lst_telescopes = Tbl_telescope.objects.all().select_related("obs_tel").order_by("name")

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {
        'lst_telescopes': lst_telescopes
    })

# Page with information about a specific telescope
def telescope_view(request, telescope_name):
    telescope = get_object_or_404(Tbl_telescope, name = telescope_name) # Get telescope by name
    instruments = Tbl_instrument.objects.filter(tel_ins = telescope) # Get instruments belonging to the telescope

    return render(request, 'dwarfs4MOSAIC/telescope.html', {
        'telescope': telescope,
        'lst_instruments': instruments
    })

# 'Instruments table' page.
def instruments_view(request):
    lst_instruments = Tbl_instrument.objects.all().select_related("tel_ins").order_by("name")

    return render(request, 'dwarfs4MOSAIC/instruments.html', {
        'lst_instruments': lst_instruments
    })

# 'Researchers table' page.
def researchers_view(request):
    lst_researchers = Tbl_researcher.objects.all()

    return render(request, 'dwarfs4MOSAIC/researchers.html', {
        'lst_researchers': lst_researchers
    })

# 'Observing runs table' page.
def observing_runs_view(request):
    lst_observing_runs = Tbl_observing_run.objects.all().select_related('instrument')

    return render(request, 'dwarfs4MOSAIC/observing_runs.html', {
        'lst_observing_runs': lst_observing_runs
    })

# Page with information about a specific observing_run
def observing_run_view(request, observing_run_name):
    observing_run = get_object_or_404(Tbl_observing_run, name = observing_run_name) # Get observing_run by name
    observing_blocks = Tbl_observing_block.objects.filter(obs_run = observing_run.id) # Get observing_blocks belonging to the observing_run
    researchers = observing_run.researchers.all() # Get researchers participating in the observing_run

    return render(request, 'dwarfs4MOSAIC/observing_run.html', {
        'observing_run': observing_run,
        'lst_observing_blocks': observing_blocks,
        'lst_researchers': researchers})

# 'Observing blocks table' page.
def observing_blocks_view(request):
    lst_observing_blocks = Tbl_observing_block.objects.all().select_related('obs_run').prefetch_related('target')

    return render(request, 'dwarfs4MOSAIC/observing_blocks.html', {
        'lst_observing_blocks': lst_observing_blocks})

# 'Target table' page.
def targets_view(request):
    lst_targets = Tbl_target.objects.all()

    return render(request, 'dwarfs4MOSAIC/targets.html', {
        'lst_targets': lst_targets})

# View for files downloading
def download_files_view(request, target_id):
    target = get_object_or_404(Tbl_target, pk=target_id)
    files = get_files(target.datafiles_path) if target.datafiles_path else []

    if request.method == "POST":
        selected_files = request.POST.getlist('checkbox_single[]')
        source_dir = os.path.join(settings.MEDIA_ROOT, target.datafiles_path)
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')

        os.makedirs(dest_dir, exist_ok=True)

        not_found = []
        copied_files = []

        for filename in selected_files:
            src_file = os.path.join(source_dir, filename)
            unique_filename = get_unique_filename(dest_dir, filename)
            dst_file = os.path.join(dest_dir, unique_filename)

            try:
                shutil.copy2(src_file, dst_file)
                copied_files.append(unique_filename)
            except FileNotFoundError:
                not_found.append(filename)
            except Exception as e:
                messages.error(request, f"Error copying {filename}: {str(e)}")

        if copied_files:
            copied_list_str = "<br>".join(copied_files)
            messages.success(
                request,
                f"<br><strong>{len(copied_files)} file(s) copied to downloads folder:</strong><br><br>{copied_list_str}"
            )

        if not_found:
            not_found_str = "<br>".join(not_found)
            messages.warning(
                request,
                f"<br><strong>{len(not_found)} file(s) not found:</strong><br><br>{not_found_str}"
            )

        return redirect('download_files_view', target_id=target_id)

    return render(request, 'dwarfs4MOSAIC/download_files.html', {
        'target': target,
        'lst_files': files,
    })