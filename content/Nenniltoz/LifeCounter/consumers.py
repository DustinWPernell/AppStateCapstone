import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from LifeCounter.models import Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.game_group_code = 'game_%s' % self.game_code

        # Join game group
        await self.channel_layer.group_add(
            self.game_group_code,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_code,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        game_code = response.get("game_code", None)
        user_id = response.get("user_id", None)
        player_data = response.get("player_data", None)

        # Send message to game group
        await self.channel_layer.group_send(self.game_group_code, {
            'type': 'send_message',
            'game_code': game_code,
            'user_id': user_id,
            'player_data': player_data,
        })

    async def send_message(self, res):
        """ Receive message from game group """

        game_code = res["game_code"]
        user_id = res["user_id"]
        player_data = res["player_data"]

        game = Game.get_by_code(game_code)

        game.set_game_player_stats(user_id, player_data)

        await self.send_json(
            {
                "game": game_code,
                "user_id": res["user_id"],
                "game_data": game.send_game_update(),
            },
        )
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
