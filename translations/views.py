from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TranslationUnit, TM

# Create your views here.
def home_page(request):  
    
    return render(request, 'home.html')

def view_tm(request, tm_id):

    selected_tm = TM.objects.get(id=tm_id)
    trans_units = TranslationUnit.objects.filter(tm=selected_tm)
    return render(request, 'tms.html', {'trans_units': trans_units})
    

def new_tm(request):
    tm = TM.objects.create()
    TranslationUnit.objects.create(source=request.POST['source_text'],
        target=request.POST['target_text'], tm=tm.id)
    return redirect('/tms/{id:d}'.format(id=tm.id))
def add_tunit(request, tm_id):
    pass
    