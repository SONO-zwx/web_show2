from django.shortcuts import render
from webApp.mirror.models import MirrorInfo


# Create your views here.
def index(request):
    shopname = request.GET.get('shopname')
    starttime = request.GET.get('starttime')
    endtime = request.GET.get('endtime')
    info = MirrorInfo.objects.filter(shopname=shopname).filter(datetimes__range=(starttime, endtime)).all().values()
    return render(request, 'mirror/index.html')