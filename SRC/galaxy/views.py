from django.http import HttpResponse

def home(request):
    return HttpResponse("Dwarfs4MOSAIC - home page")

def observatory(request):
    return HttpResponse("Dwarfs4MOSAIC - Observatories page")

def telescope(request):
    return HttpResponse("Dwarfs4MOSAIC - Telescopes page")

def instrument(request):
    return HttpResponse("Dwarfs4MOSAIC - Instruments page")