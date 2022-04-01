from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chat.views import is_room_occupied
from .models import ChatUser, ChatRoom, UserAndRoom
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from io import StringIO
import time
import sys
import os

@login_required
def shared_editing(request, room_name):
    print(room_name, 'was visited')
    if not is_room_occupied(room_name): #if not occupied, ask to set a password
       return render(request, 'shared.html', {
           'room_name': room_name,
           'set_pass': True,
       }) 
    else: #else ask user to enter the password
        chat_user = ChatUser.objects.get(chat_user=request.user)
        print(chat_user)
        chat_rooms = UserAndRoom.objects.filter(chat_user=chat_user)
        print(chat_rooms)
        for room in chat_rooms:
            if str(room.chat_room) == room_name:
                #user is already authorized
                return render(request, 'shared.html',{
                    'room_name': room_name,
                    'user': request.user
                })
        #user is not authorized, ask for password
        return render(request, 'shared.html', {
            'room_name': room_name,
            'get_pass': True,
        })


@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        code = body['code']
        out = StringIO() 
        sys.stdout = out
        try:
            exec(code)
            results = out.getvalue()
            return JsonResponse({"code": 0, "msg": "Successfully ran code", "results": results}, status=200)
        except:
            return JsonResponse({"code": 1, "msg": "Could not execute the code"}, status=400)