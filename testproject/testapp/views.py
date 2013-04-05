from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'authenticated': request.user.is_authenticated()
    })
