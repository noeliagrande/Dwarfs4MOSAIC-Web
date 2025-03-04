from django.http import HttpResponse

def home(request):
    return HttpResponse("Dwarfs4MOSAIC - home page")