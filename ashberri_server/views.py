from django.http import HttpResponse
from requests import Response
from rest_framework.views import APIView


class home(APIView):
    def get(self, request, *args,**kwargs):
        return HttpResponse('Welcome to the Ashberri server',content_type ='application/json')
    