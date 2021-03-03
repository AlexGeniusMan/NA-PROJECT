from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from .permissions import *
from .serializers import *
import os
from django.views.generic.base import View
from django.http import HttpResponse


class ShowRecentNewsView(APIView):
    """
    Shows recent messages
    """

    def get(self, request):
        messages = Message.objects.all()
        messages = MessageSerializer(messages, context={'request': request}, many=True).data
        return Response(messages)
        # return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})


class ReactAppView(View):

    def get(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                File index.html not found ! Build your React app !
                """,
                status=501,
            )
