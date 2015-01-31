from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TranslationUnit

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def view_tms(request):
    trans_units = TranslationUnit.objects.all()
    return render(request, 'tms.html', {'trans_units': trans_units})
def new_tm(request):
    TranslationUnit.objects.create(
        source=request.POST['source_text'],
        target=request.POST['target_text'])
    return redirect('/tms/new-translation-memory/')
    