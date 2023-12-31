import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['v_name']
        print('self.room_name: '+str(self.room_name))
        self.room_group_name = f'video_{self.room_name}'
        print('self.room_group_name: '+str(self.room_group_name))
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self,close_code):
        #Leave room group
        print("disconnect")
        print("close_code: "+str(close_code))
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        # Send Message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'video_message',
                'message' : text_data,
            }
        )
    
    #Receive message from room group
    async def video_message(self,event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message':message
        }))
