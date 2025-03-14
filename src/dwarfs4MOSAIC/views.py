from django.db import connection
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Tbl_observatory, Tbl_telescope, Tbl_instrument
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

    return render(request, 'dwarfs4MOSAIC/observatories.html', {'lst_observatories': lst_observatories})

# Page with telescopes for a specific observatory
def observatory_view(request, observatory_name):
    observatory = get_object_or_404(Tbl_observatory, name = observatory_name) # Get observatory by name
    telescopes = Tbl_telescope.objects.filter(obs_tel = observatory.id) # Get telescopes belonging to the observatory
    prev_page = request.META.get('HTTP_REFERER', '/') # Get URL of previous page

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory_name': observatory_name,
        'lst_telescopes': telescopes,
        'previous_page': prev_page
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

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {'lst_telescopes': lst_telescopes})

# Page with information about a specific telescope
def telescope_view(request, telescope_name):
    telescope = get_object_or_404(Tbl_telescope, name = telescope_name) # Get telescope by name
    instruments = Tbl_instrument.objects.filter(tel_ins = telescope.id) # Get instruments belonging to the telscope

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

    return render(request, 'dwarfs4MOSAIC/instruments.html', {'lst_instruments': lst_instruments})

# Page with information about a specific instrument
def instrument_view(request, instrument_name):
    instrument = get_object_or_404(Tbl_instrument, name=instrument_name) # Get instrument by name
    return render(request, 'dwarfs4MOSAIC/instrument.html', {'instrument': instrument})

# 'Members table' page.
def members_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_member ORDER BY name")
        lst_members = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/members.html', {'lst_members': lst_members})

# 'Observing runs table' page.
def observing_runs_view(request):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_observing_run ORDER BY name")

        cursor.execute("""
            SELECT observing_run.*, member.name AS leader_name 
            FROM dwarfs4MOSAIC_Tbl_observing_run observing_run
            LEFT JOIN dwarfs4MOSAIC_Tbl_member member 
            ON observing_run.leader_id = member.id
            ORDER BY observing_run.name
        """)

        lst_observing_runs = dictfetchall(cursor)

    return render(request, 'dwarfs4MOSAIC/observing_runs.html', {'lst_observing_runs': lst_observing_runs})

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

    return render(request, 'dwarfs4MOSAIC/observing_blocks.html', {'lst_observing_blocks': lst_observing_blocks})