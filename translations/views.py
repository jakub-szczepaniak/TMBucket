from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from translations.models import TransUnit, TM

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_tms(request, tm_id):
    tm_to_show = TM.objects.get(id=tm_id)
    if request.method == 'POST':
        new_transunit =TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'],
        tm=tm_to_show)
        return redirect('/tms/{:d}/'.format(tm_to_show.id))
        
    return render(request, 'tms.html', {'tm': tm_to_show})
def new_tm(request):
    new_tm = TM.objects.create()
    new_transunit =TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'],
        tm=new_tm)
    try:
        new_transunit.full_clean()
        new_transunit.save()
    except ValidationError:
        new_tm.delete()
        error = "You can't submit empty string"
        return render(request, 'home.html', {'error' : error })
    return redirect('/tms/{:d}/'.format(new_tm.id))


    