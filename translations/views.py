from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TransUnit, TM

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_tms(request, tm_id):
    tm_to_show = TM.objects.get(id=tm_id)
    return render(request, 'tms.html', {'tm': tm_to_show})
def new_tm(request):
    new_tm = TM.objects.create()
    TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'],
        tm=new_tm)
    return redirect('/tms/{:d}/'.format(new_tm.id))
def add_transunit(request, tm_id):
    existing_tm = TM.objects.get(id=tm_id)
    TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'],
        tm=existing_tm)
    return redirect('/tms/{:d}/'.format(existing_tm.id))
    