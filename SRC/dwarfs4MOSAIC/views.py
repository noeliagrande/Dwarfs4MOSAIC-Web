from django.db import connection
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Tbl_observatory, Tbl_telescope, Tbl_instrument

# 'Home' page.
def home_view(request):
    return render(request, 'dwarfs4MOSAIC/home.html')

# 'Observatories table' page.
def observatories_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_observatory")
        rows = cursor.fetchall()

    return render(request, 'dwarfs4MOSAIC/observatories.html',
                  {'lst_observatories': rows})

# Page with telescopes for a specific observatory
def observatory_view(request, observatory_name):
    observatory = get_object_or_404(Tbl_observatory, name = observatory_name) # Get observatory by name
    telescopes = Tbl_telescope.objects.filter(obs_tel = observatory.id) # Get telescopes belonging to the observatory
    prev_page = request.META.get('HTTP_REFERER', '/') # Get URL of previous page

    return render(request, 'dwarfs4MOSAIC/observatory.html', {
        'observatory': observatory,
        'lst_telescopes': telescopes,
        'previous_page': prev_page
    })

# 'Telescopes table' page.
def telescopes_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_telescope")
        rows = cursor.fetchall()

    return render(request, 'dwarfs4MOSAIC/telescopes.html', {'lst_telescopes': rows})

# Page with information about a specific telescope
def telescope_view(request, telescope_name):
    telescope = get_object_or_404(Tbl_telescope, name = telescope_name) # Get telescope by name
    instruments = Tbl_instrument.objects.filter(tel_ins = telescope.id) # Get instruments belonging to the telscope
    prev_page = request.META.get('HTTP_REFERER', '/') # Get URL of previous page

    return render(request, 'dwarfs4MOSAIC/telescope.html', {
        'telescope': telescope,
        'lst_instruments': instruments,
        'previous_page': prev_page
    })

# 'Instruments table' page.
def instruments_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dwarfs4MOSAIC_Tbl_instrument")
        rows = cursor.fetchall()

    return render(request, 'dwarfs4MOSAIC/instruments.html', {'lst_instruments': rows})

# Page with information about a specific instrument
def instrument_view(request, instrument_name):

    ins = get_object_or_404(Tbl_instrument, name=instrument_name) # Get instrument by name
    prev_page = request.META.get('HTTP_REFERER', '/') # Get URL of previous page

    return render(request, 'dwarfs4MOSAIC/instrument.html', {'Tbl_instrument': ins, 'previous_page': prev_page})
