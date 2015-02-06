from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from translations.models import TransUnit, TM
from translations.forms import TransUnitForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': TransUnitForm()})
def view_tms(request, tm_id):
    tm_to_show = TM.objects.get(id=tm_id)
    error = None
    if request.method == 'POST':
        new_transunit =TransUnit(
                source=request.POST['source'],
                target=request.POST['target'],
                tm=tm_to_show)
        try:
            new_transunit.full_clean()
            new_transunit.save()
            return redirect(tm_to_show)
        except ValidationError:
            error = "You can't submit empty string"
        
        
    return render(request, 'tms.html', {'tm': tm_to_show, 'error': error})
def new_tm(request):
    new_tm = TM.objects.create()
    new_transunit =TransUnit(
        source=request.POST['source'],
        target=request.POST['target'],
        tm=new_tm)
    try:
        new_transunit.full_clean()
        new_transunit.save()
    except ValidationError:
        new_tm.delete()
        error = "You can't submit empty string"
        return render(request, 'home.html', {'error' : error })
    return redirect(new_tm)


    