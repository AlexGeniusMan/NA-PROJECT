from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from .permissions import *
from .serializers import *
import os
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from rest_framework.permissions import IsAuthenticated


class ShowRecentMessagesView(APIView):
    """
    Shows recent messages
    """

    def post(self, request):
        find_by_letters = request.POST['find_by_letters']

        data = []
        next_page = 1
        previous_page = 1
        products = Message.objects.filter(
            Q(title__icontains=find_by_letters) |
            Q(title__icontains=find_by_letters.capitalize()) |
            Q(title__icontains=find_by_letters.lower()) |
            Q(title__icontains=find_by_letters.upper())
        )

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 3)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = MessageSerializer(data, context={'request': request}, many=True)

        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({
            'products': serializer.data,
            'count': paginator.count,
            'numpages': paginator.num_pages,
            'nextlink': '/api/recent_news?page=' + str(next_page),
            'prevlink': '/api/recent_news?page=' + str(previous_page)
        })


class ShowMessagesOfCurrentCategoryView(APIView):
    """
    Shows recent messages of current category
    """

    def post(self, request):
        category = request.POST['category']

        data = []
        next_page = 1
        previous_page = 1
        products = Message.objects.filter(
            Q(category=category)
        )

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 1)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = MessageSerializer(data, context={'request': request}, many=True)

        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({
            'products': serializer.data,
            'count': paginator.count,
            'numpages': paginator.num_pages,
            'nextlink': '/api/recent_news?page=' + str(next_page),
            'prevlink': '/api/recent_news?page=' + str(previous_page)
        })


class AddNewMessageView(APIView):
    """
    Adds new message
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            title = request.data['title']
            img = request.FILES['img']
            short_description = request.data['short_description']
            content = request.data['content']
            category = request.POST['category']

            Message.objects.create(title=title, img=img, short_description=short_description, content=content,
                                   category=category)

            return Response(True)
        except:
            return Response(False)


class ShowCurrentMessageView(APIView):
    """
    Shows current message
    """

    def post(self, request):
        try:
            message_pk = request.POST['message_pk']

            message = Message.objects.get(pk=message_pk)
            message = MessageSerializer(message, context={'request': request}).data

            return Response({"data": message, "status": status.HTTP_200_OK})
        except:
            return Response({"error_message": "MESSAGE NOT FOUND", "status": status.HTTP_404_NOT_FOUND})


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
