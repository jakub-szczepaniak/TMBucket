from django.shortcuts import render, redirect
from django.http import HttpResponse
from translations.models import TranslationUnit

# Create your views here.
def home_page(request):
    if request.method=='POST':
        
        
        TranslationUnit.objects.create(source=request.POST['source_text'],
                                    target=request.POST['target_text'])
        
        return redirect('/')    
    trans_units = TranslationUnit.objects.all()
    return render(request, 'home.html', {'trans_units': trans_units})
    