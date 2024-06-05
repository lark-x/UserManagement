from django.shortcuts import render


def record_list(request):
    if request.method == 'GET':
        return render(request, 'record_list.html')
