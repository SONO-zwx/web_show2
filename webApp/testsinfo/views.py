from rest_framework.views import APIView
from django.shortcuts import render


class testinfo(APIView):
    def get(self, request):
        return render(request, 'testsinfo/testinfo.html', {'limits': request.session.get('limits')})

    def post(self, request):
        pass


