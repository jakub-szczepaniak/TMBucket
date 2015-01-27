from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    if request.method=='POST':
        return render(request, 'home.html', {'source_item_text' : request.POST['source_text'],
                                             'target_item_text' : request.POST['target_text']
                                            })
    return render(request, 'home.html')