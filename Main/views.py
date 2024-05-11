import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Offer
from .XML import parse_offers, parse_categories
from django.contrib.auth.decorators import user_passes_test




def index(request):
    offers = Offer.objects.all()
    context = {"name": "Main", "offers": offers}
    return render(request, 'Main/index.html' , context)

@user_passes_test(lambda u: u.is_superuser)
def import_file(request):
    if request.method == 'POST':
        try: file = request.FILES['file']
        except: return redirect('index')

        media_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
        
        file_path = os.path.join(media_dir, file.name)

        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


        # parse_categories(xml_file_path=file_path)
        parse_offers(xml_file_path=file_path)
        # print([f.id for f in offers])

    return redirect('index')
