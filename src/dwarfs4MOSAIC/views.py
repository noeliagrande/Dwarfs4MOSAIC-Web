from django.db import connection
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import *
from .utils import dictfetchall

# 'Home' page.
def home_view(request):
    return render(request, 'dwarfs4MOSAIC/home.html')

# 'Database tables' page.
def database_view(request):
    return render(request, 'dwarfs4MOSAIC/database.html')

# 'Observatories table' page.
def observatories_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_observatory ORDER BY name")
        lst_observatories = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/observatories.html', {
        'lst_observatories': lst_observatories
    })

# Page with telescopes for a specific observatory
def observatory_view(request, observatory_name):
    observatory = get_object_or_404(Tbl_observatory, name = observatory_name) # Get observatory by name
    telescopes = Tbl_telescope.objects.filter(obs_tel = observatory.id) # Get telescopes belonging to the observatory

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory_name': observatory_name,
        'lst_telescopes': telescopes
    })

# 'Telescopes table' page.
def telescopes_view(request):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_telescope")
        cursor.execute("""
            SELECT telescope.*, observatory.name AS observatory_name 
            FROM dwarfs4MOSAIC_Tbl_telescope telescope
            JOIN dwarfs4MOSAIC_Tbl_observatory observatory
            ON telescope.obs_tel_id = observatory.id
            ORDER BY name
        """)
        lst_telescopes = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {
        'lst_telescopes': lst_telescopes
    })

# Page with information about a specific telescope
def telescope_view(request, telescope_name):
    telescope = get_object_or_404(Tbl_telescope, name = telescope_name) # Get telescope by name
    instruments = Tbl_instrument.objects.filter(tel_ins = telescope.id) # Get instruments belonging to the telescope

    return render(request, 'dwarfs4MOSAIC/telescope.html', {
        'telescope': telescope,
        'lst_instruments': instruments
    })

# 'Instruments table' page.
def instruments_view(request):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_instrument")
        cursor.execute("""
            SELECT instrument.*, telescope.name AS telescope_name 
            FROM dwarfs4MOSAIC_Tbl_instrument instrument
            JOIN dwarfs4MOSAIC_Tbl_telescope telescope
            ON instrument.tel_ins_id = telescope.id
            ORDER BY name
        """)
        lst_instruments = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/instruments.html', {
        'lst_instruments': lst_instruments
    })

# Page with information about a specific instrument
def instrument_view(request, instrument_name):
    instrument = get_object_or_404(Tbl_instrument, name=instrument_name) # Get instrument by name
    return render(request, 'dwarfs4MOSAIC/instrument.html', {
        'instrument': instrument
    })

# 'Researchers table' page.
def researchers_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_researcher ORDER BY name")
        lst_researchers = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/researchers.html', {
        'lst_researchers': lst_researchers
    })

# 'Observing runs table' page.
def observing_runs_view(request):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_observing_run ORDER BY name")
        cursor.execute("""
            SELECT observing_run.*, instrument.name AS instrument_name 
            FROM dwarfs4MOSAIC_Tbl_observing_run observing_run
            JOIN dwarfs4MOSAIC_Tbl_instrument instrument
            ON observing_run.instrument_id = instrument.id
            ORDER BY observing_run.name
        """)

        lst_observing_runs = dictfetchall(cursor)
        print(lst_observing_runs)

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
        'lst_researchers': researchers
    })

# 'Observing blocks table' page.
def observing_blocks_view(request):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_observing_block ORDER BY name")
        cursor.execute("""
            SELECT observing_block.*, observing_run.name AS observing_run_name 
            FROM dwarfs4MOSAIC_Tbl_observing_block observing_block
            LEFT JOIN dwarfs4MOSAIC_Tbl_observing_run observing_run 
            ON observing_block.obs_run_id = observing_run.id
            ORDER BY observing_block.start_time
        """)

        lst_observing_blocks = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/observing_blocks.html', {
        'lst_observing_blocks': lst_observing_blocks
    })