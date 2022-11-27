from asyncio.windows_events import NULL
import email
from multiprocessing import context
from urllib import request
from django.shortcuts import render

def home(request):
    context = {
        "titulo": "Sena 2022",
	    "nombreForm": "BIENVENIDO",
    }
    return render(request, 'home.html', context)