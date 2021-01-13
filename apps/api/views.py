from django.shortcuts import render
from django.http import JsonResponse

def root(request):
    return JsonResponse({"projeto": 'Sophia' })

