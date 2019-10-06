from datetime import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Registration
from .forms import RegoForm

# Create your views here.
def index(request):
    r = len(Registration.objects.all())
    p = settings.NO_PLACES - r

    if 'registered' in request.session.keys():
        if request.session['registered']:
            return render(request, 'rego/registered.html')

    if timeout():
        return render(request, 'rego/timeout.html')

    if p == 0:
        return render(request, 'rego/full.html')

    if request.method == 'POST':
        form = RegoForm(request.POST)
        if form.is_valid():
            # Save stuff
            form.save()
            request.session['registered'] = form.cleaned_data['email']
            return render(request, 'rego/registered.html')
        return render(request, 'rego/index.html',
                {'form': form, 'places_left': p})

    form = RegoForm()
    return render(request, 'rego/index.html',
            {'form': form, 'places_left': p})


def timeout():
    """ d0 is the registration close date (inclusive) """
    d0 = datetime.strptime(settings.TIMEOUT_DATE, '%Y-%m-%d')
    if datetime.now() < d0:
        return False
    return True


def cancel(request):
    """ Cancel booking and return to homepage """
    user_email = request.session['registered']
    r = Registration.objects.get(email=user_email)
    r.delete()
    request.session['registered'] = None
    return redirect('/')


def test_view(request):
    """ Test out an html template """
    return render(request, 'rego/registered.html')
