from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Stock_apply(APIView):
    def get(self, request):
        return render(request, 'storage/stock_apply.html')

    def post(self, request):
        return render(request, 'storage/stock_apply.html')


class Out_apply(APIView):
    def get(self, request):
        return render(request, 'storage/out_apply.html')

    def post(self, request):
        return render(request, 'storage/out_apply.html')

class Stock_lists(APIView):
    def get(self, request):
        info = [i for i in range(5)]
        return render(request, 'storage/stock_lists.html', {'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        return render(request, 'storage/stock_lists.html')

class Inventory(APIView):
    def get(self, request):
        info = [i for i in range(5)]
        return render(request, 'storage/inventory.html', {'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        return render(request, 'storage/inventory.html')