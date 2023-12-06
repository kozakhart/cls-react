from django.shortcuts import render
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
import slat.box_api.box_api as box_api
from slat.box_api.box_api import *
# Create your views here.
def create_slats(request):
    if request.method == 'POST':
        form = SLATForm_Forms(request.POST)

        firstname = (request.POST.get('firstname', False))
        lastname = (request.POST.get('lastname', False))
        byu_id = (request.POST.get('byuid', False))
        language = (request.POST.get('language', False))

        initial_date = (request.POST.get('thesis'))
        format_initial = datetime.strptime(initial_date, '%Y-%m-%d').date()
        thesis_date = datetime.strftime(format_initial, '%m-%d-%Y')

        transcript = request.FILES['transcript']
        opi_rating = request.FILES['opi']

        # print(transcript.size)
        # print(transcript.name)

        client = box_api.create_client()
        FileSystemStorage(location="/tmp").save(transcript.name, transcript)
        FileSystemStorage(location="/tmp").save(opi_rating.name, opi_rating)
        box_api.create_pdf(full_name=firstname + " " + lastname, byu_id=byu_id, language=language, thesis=thesis_date)
        files = []
        files.append("/tmp/" + transcript.name)
        files.append("/tmp/" + opi_rating.name)
        files.append("/tmp/" + f"{firstname} {lastname} Information.pdf")

        slat_folder = '185240535599'
        box_api.upload_files(client=client, student_name=firstname + " " + lastname + "(" + byu_id + ")", files=files, slat_folder=slat_folder)
        return render(request, 'slats_receipt.html', {'form': form})
    else:
        form = SLATForm_Forms()

    return render(request, 'slats.html', {'form': form})

def slats_receipt(request):
    get_template('slats_receipt.html')
    return render(request, 'slats_receipt.html')