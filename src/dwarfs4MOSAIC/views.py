from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import *

# 'Home' page.
def home_view(request):
    #return render(request, 'dwarfs4MOSAIC/home.html')

    context = {}
    if request.user.is_authenticated:
        context['authenticated'] = True
        context['lst_targets'] = Tbl_target.objects.prefetch_related('observing_blocks__obs_run')
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
