from django.http import HttpResponse


def index(request):
    return HttpResponse("РГАУ-МСХА имени К. А. Тимирязева")


