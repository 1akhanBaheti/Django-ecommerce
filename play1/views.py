from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product,OrderItem
from django.db.models import Q,F

def sendHtml(request):
    response =OrderItem.objects.fi

    return render(request,'response.html',{
        'response':response,
    })