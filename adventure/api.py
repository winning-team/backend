from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
# from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
from ratelimit.decorators import ratelimit
import json
import pusher

pusher = pusher.Pusher(
    app_id=config('PUSHER_APP_ID'),
    key=config('PUSHER_KEY'),
    secret=config('PUSHER_SECRET'),
    cluster=config('PUSHER_CLUSTER'),
    ssl=True
)


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'username': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'x': player.x, 'y': player.y, 'room_id': room.id, 'sprite_id': player.user.sprite_id, 'n': room.n_to, 's': room.s_to, 'e': room.e_to, 'w': room.w_to}, safe=True)


# @csrf_exempt
@ratelimit(rate=None)
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    moveRooms = False
    moveInRoom = False
    prevX = player.x
    prevY = player.y
    direction = data['direction']
    room = player.room()
    nextRoomID = None

    def movePusher(id, x, y, shouldRemove):
        print(
            f'pushing move message to channel: move_{id} event: move_{id}_event')
        pusher.trigger(f'move_{id}', f'move_{id}_event', {
            'player': {'username': player.user.username, 'sprite_id': player.user.sprite_id, 'x': x, 'y': y, 'prevX': None if not shouldRemove else prevX, 'prevY': None if not shouldRemove else prevY}})

    if direction == "n":
        if player.x == 1 and player.y == 2:
            moveRooms = True
        if player.y != 2:
            moveInRoom = True
        nextRoomID = room.n_to
    elif direction == "s":
        if player.x == 1 and player.y == 0:
            moveRooms = True
        if player.y != 0:
            moveInRoom = True
        nextRoomID = room.s_to
    elif direction == "e":
        if player.x == 2 and player.y == 1:
            moveRooms = True
        if player.x != 2:
            moveInRoom = True
        nextRoomID = room.e_to
    elif direction == "w":
        if player.x == 0 and player.y == 1:
            moveRooms = True
        if player.x != 0:
            moveInRoom = True
        nextRoomID = room.w_to
    if nextRoomID:
        nextRoom = Room.objects.get(id=nextRoomID)
    players = room.playerNames(player_id)
    if moveRooms and nextRoomID is not None and nextRoomID > 0:
        currentPlayerUUIDs = room.playerUUIDs(player_id)

        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        if len(currentPlayerUUIDs):
            pusher.trigger(f'room_{room.id}', f'room_{room.id}_event', {
                           'message': f'[{player.user.username}] exited to the {dirs[direction]}.'})
            movePusher(room.id, None, None, True)
        if len(nextPlayerUUIDs):
            pusher.trigger(f'room_{nextRoomID}', f'room_{nextRoomID}_event', {
                           'message': f'[{player.user.username}] entered from the {reverse_dirs[direction]}.'})
            movePusher(nextRoomID, player.x, player.y, False)
        player.currentRoom = nextRoomID
        if direction == 'n':
            player.x = 1
            player.y = 0
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 'e':
            player.x = player.x
            player.x = 0
            player.y = 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 's':
            player.x = 1
            player.y = 2
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 'w':
            player.x = 2
            player.y = 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        players = nextRoom.playerNames(player_id)
        return JsonResponse({'room_id': nextRoomID, 'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'error_msg': "", "x": player.x, "y": player.y, 'sprite_id': player.user.sprite_id, 'n': nextRoom.n_to, 's': nextRoom.s_to, 'e': nextRoom.e_to, 'w': nextRoom.w_to}, safe=True)
    elif moveInRoom:
        if direction == 'n':
            player.y = player.y + 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 'e':
            player.x = player.x + 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 's':
            player.y = player.y - 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        elif direction == 'w':
            player.x = player.x - 1
            player.save()
            movePusher(room.id, player.x, player.y, True)
        print(room.id)
        return JsonResponse({'room_id': room.id, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "", "x": player.x, "y": player.y, 'sprite_id': player.user.sprite_id}, safe=True)
    else:
        return JsonResponse({'room_id': room.id, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way.", "x": player.x, "y": player.y, 'sprite_id': player.user.sprite_id}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    room = player.room()
    data = json.loads(request.body)
    message = data['message']
    pusher.trigger(f'room_{room.id}', f'room_{room.id}_event', {
        'message': f'[{player.user.username}]: {message}'})
    return JsonResponse({'message': 'Message sent!'}, safe=True, status=200)


@api_view(["GET"])
def map(request):
    player = request.user.player
    room = player.room()
    if not player.currentWorld:
        player.initialize()
        player.save()
    map = World.objects.get(id=player.currentWorld).map
    return JsonResponse({'playerCoords': {'x': player.room().x, 'y': player.room().y}, 'Coordinates': json.loads(map)}, safe=True)
