from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TransUnit

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_tms(request):
    trans_units = TransUnit.objects.all()
    return render(request, 'tms.html', {'trans_units': trans_units})
def new_tm(request):
    TransUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'])
    return redirect('/tms/new-translation-memory/')
    