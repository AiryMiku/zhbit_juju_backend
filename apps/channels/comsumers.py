#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: comsumers.py
# @Software: PyCharm

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):
    chats = dict()

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # 将用户添加至聊天组信息chats中
        try:
            ChatConsumer.chats[self.group_name].add(self)
        except:
            ChatConsumer.chats[self.group_name] = set([self])

        print(ChatConsumer.chats)
        # 创建连接时调用
        await self.accept()

    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 将该客户端移除聊天组连接信息
        ChatConsumer.chats[self.group_name].remove(self)
        await self.close()


class PushConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(self)
        self.group_name = self.scope['url_route']['kwargs']['id']
        print(self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        # await push('airy','heihei')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        print(PushConsumer.groups)

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            "event": event['event']
        }))


def push(id, event):
    print(id, event)
    channel_layer = get_channel_layer()
    print(get_channel_layer())
    async_to_sync(channel_layer.group_send)(
        id,
        {
            "type": "push.message",
            "event": event
        }
    )


class TestConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        await self.accept()
        print("Hello world")
        await self.send("Hello world")

    async def disconnect(self, code):

        print("Bye")
        await self.send("Bye")

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print("receive -> "+text_data)
        message = text_data

        await self.send_json(json.dumps({
            'message': message
        }))

    async def close(self, code=None):
        print("close")


