from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TransUnit, TM

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_tms(request):
    trans_units = TransUnit.objects.all()
    return render(request, 'tms.html', {'trans_units': trans_units})
def new_tm(request):
    tm = TM.objects.create()
    TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'],
        tm=tm)
    return redirect('/tms/new-translation-memory/')
    