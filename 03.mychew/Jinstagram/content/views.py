from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed
# Create your views here.

class Main(APIView):
    def get(self, request) :
        feed_list = Feed.objects.all().order_by('-id')  # id 역순으로 데이터를 가져옴.

        return render(request, "Jinstagram/main.html", context=dict(feeds=feed_list))