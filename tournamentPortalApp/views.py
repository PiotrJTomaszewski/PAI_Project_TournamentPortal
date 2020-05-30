from django.shortcuts import render

def index(request):
    context = {
    }
    return render(request, 'tournaments/index.html', context)

def tournamentList(request):
    context = {

    }
    return render(request, 'tournaments/list.html', context)
