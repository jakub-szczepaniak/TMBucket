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
    form = TransUnitForm()
    if request.method == 'POST':
        form = TransUnitForm(data=request.POST)
        if form.is_valid():
            new_transunit =TransUnit.objects.create(
                source=request.POST['source'],
                target=request.POST['target'],
                tm=tm_to_show)
            return redirect(tm_to_show)
    
    return render(request, 'tms.html', {'tm': tm_to_show, 'form': form})
def new_tm(request):
    form = TransUnitForm(data = request.POST)

    if form.is_valid():
        new_tm = TM.objects.create()
        TransUnit.objects.create(
            source=request.POST['source'], 
            target=request.POST['target'],
            tm=new_tm)
        return redirect(new_tm)
    else:
        return render(request,'home.html', {'form': form})
    

    