from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from .permissions import *
from .serializers import *


class ShowRecentNewsView(APIView):
    """
    Shows recent messages
    """

    def get(self, request):
        messages = Message.objects.all()
        messages = MessageSerializer(messages, context={'request': request}, many=True).data
        return Response(messages)
        # return Response({"error_code": 'YOUR TICKET IS EXPIRED', "status": status.HTTP_403_FORBIDDEN})
