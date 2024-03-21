from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def Agile (request):
    template = loader.get_template('agile.html')
    return HttpResponse(template.render())
