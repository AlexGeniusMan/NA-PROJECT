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


class GetMostPopularAndPinnedMessages(APIView):
    """
    Gets most popular and pinned messages
    """

    def post(self, request):
        most_popular_messages = Message.objects.all().order_by('-view_counter')[:3]
        most_popular_messages = MessageSerializer(most_popular_messages, context={'request': request}, many=True).data

        # most_popular_messages = Message.objects.all().order_by('-view_counter')[:3]
        # most_popular_messages = MessageSerializer(most_popular_messages, context={'request': request}, many=True).data

        return Response({
            'most_popular_messages': most_popular_messages
        })


class UpdateViewCounterView(APIView):
    """
    Updates message's view counter
    """

    def post(self, request, message_id):
        message = Message.objects.get(pk=message_id)
        message.view_counter += 1
        message.save()

        return Response(True)


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


class AddOrChangeMessageView(APIView):
    """
    Adds or changes message
    """

    permission_classes = (IsAuthenticated,)

    def get_message(self, request, message_pk):
        try:
            message = Message.objects.get(pk=message_pk)
            message = MessageSerializer(message, context={'request': request}).data

            return message
        except:
            return False

    def post(self, request):
        try:
            title = request.data['title']
            img = request.FILES['img']
            short_description = request.data['short_description']
            content = request.data['content']
            category = request.POST['category']

            message = Message.objects.create(title=title, img=img, short_description=short_description, content=content,
                                             category=category)

            return Response(self.get_message(request, message.pk))
        except:
            return Response(False)

    def put(self, request):
        try:
            message_pk = request.POST['message_pk']
            message = Message.objects.get(pk=message_pk)

            try:
                if request.data['img'] == 'null':
                    message.img = None
                else:
                    message.img = request.FILES['img']
            except:
                pass

            message.title = request.data['title']
            message.short_description = request.data['short_description']
            message.content = request.data['content']
            message.category = request.POST['category']

            message.save()

            return Response(self.get_message(request, message.pk))
        except:
            return Response(False)

    def delete(self, request):
        try:
            message_pk = request.POST['message_pk']
            message = Message.objects.get(pk=message_pk)
            message.delete()

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
