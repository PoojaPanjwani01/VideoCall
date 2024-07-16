# from django.shortcuts import render
# from django.http import JsonResponse
# from agora_token_builder import RtcTokenBuilder
# import random
# import time


# def getToken(request):
#     appId = 'd3e454e8700d41bfac19bd634286b38b'
#     appCertificate = '3158296969e843cfa8603477c47d4215'
#     channelName = request.GET.get('channel')
#     uid = random.randint(1,230)
#     expirationTimeInSeconds = 3600 * 72
#     currentTimeStamp = time.time()
#     privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
#     role = 1
    
#     token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
#     return JsonResponse({'token':token, 'uid':uid}, safe=False)
    
# def lobby(request):
#     return render(request, 'base/lobby.html')

# def room(request):
#     return render(request, 'base/room.html')



from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
def generate_random_uid():
    return random.randint(1, 230)

def generate_agora_token(app_id, app_certificate, channel_name, uid, role=1, expiration_seconds=3600 * 72):
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_seconds

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
    return token

def getToken(request):
    app_id = 'd3e454e8700d41bfac19bd634286b38b'
    app_certificate = '3158296969e843cfa8603477c47d4215'
    channel_name = request.GET.get('channel')
    uid = generate_random_uid()

    token = generate_agora_token(app_id, app_certificate, channel_name, uid)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name' :data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    
    member = RoomMember.objects.get(uid=uid, room_name=room_name,)
    
    name = member.name
    return JsonResponse({'name' :member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)