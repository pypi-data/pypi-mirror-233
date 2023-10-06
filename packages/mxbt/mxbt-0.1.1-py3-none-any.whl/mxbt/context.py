from nio import MatrixRoom, Event, RoomMessageText
from dataclasses import dataclass, field
from typing import List
from .api import Api

@dataclass
class Context:

    api: Api
    room: MatrixRoom
    event: Event
    body: str=str()
    command: str=str()
    args: List[str]=field(
        default_factory=lambda: list()
    )

    async def send_text(self, 
                        body: str, 
                        reply: bool=False,
                        edit: bool=False) -> None:
        await self.api.send_text(
            self.room.room_id,
            body,
            reply_to=self.event.event_id if reply else "",
            edit_id=self.event.event_id if edit else ""
        )

    async def send_markdown(self, 
                            body: str, 
                            reply: bool=False, 
                            edit: bool=False) -> None:
        await self.api.send_markdown(
            self.room.room_id,
            body,
            reply_to=self.event.event_id if reply else "",
            edit_id=self.event.event_id if edit else ""
        )

    async def send_image(self, 
                         filepath: str, 
                         reply: bool=False, 
                         edit: bool=False) -> None:
        await self.api.send_image(
            self.room.room_id,
            filepath,
            self.event.event_id if reply else "",
            self.event.event_id if edit else ""
        )

    async def send_video(self, 
                         filepath: str, 
                         reply: bool=False, 
                         edit: bool=False) -> None:
        await self.api.send_video(
            self.room.room_id,
            filepath,
            self.event.event_id if reply else "",
            self.event.event_id if edit else ""
        )

    async def send_reaction(self, body: str) -> None:
        await self.api.send_reaction(
            self.room.room_id,
            self.event.event_id,
            body
        )

    @staticmethod
    def __parse_command(message: RoomMessageText) -> tuple:
        args = message.body.split(" ")
        command = args[0]
        if len(args) > 1:
            args = args[1:]
        return command, args

    @staticmethod
    def from_command(api: Api, room: MatrixRoom, message: RoomMessageText):
        command, args = Context.__parse_command(message)
        return Context(
            api=api,
            room=room, 
            event=message,
            body=message.body,
            command=command,
            args=args
        )

    @staticmethod
    def from_text(api: Api, room: MatrixRoom, message: RoomMessageText):
        return Context(
            api=api,
            room=room,
            event=message,
            body=message.body
        )

