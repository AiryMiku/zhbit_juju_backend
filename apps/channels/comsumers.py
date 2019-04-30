#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Peihua Tang
# @FileName: comsumers.py
# @Software: PyCharm

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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


class PushConsumer(AsyncConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        print(PushConsumer.chats)

    async def push_message(self, event):
        print(event)
        await self.send({
            "event": event['event']
        })


def push(username, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
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

    async def close(self, code=None):
        print("close")
