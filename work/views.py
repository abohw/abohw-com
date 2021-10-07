from django.shortcuts import render


def workHome(request):

    return render(request, 'work/index.html', { })