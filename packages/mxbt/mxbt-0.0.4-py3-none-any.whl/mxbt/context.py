from nio import MatrixRoom, Event, RoomMessage, RoomMessageText
from dataclasses import dataclass, field
from typing import List

@dataclass
class Context:
   
    room: MatrixRoom
    event: Event
    command: str=str()
    args: List[str]=field(
        default_factory=lambda: list()
    )

    @staticmethod
    def __parse_command(message: RoomMessageText) -> tuple:
        args = message.body.split(" ")
        command = args[0]
        if len(args) > 1:
            args = args[1:]
        return command, args

    @staticmethod
    def from_command(room: MatrixRoom, message: RoomMessageText):
        command, args = Context.__parse_command(message)
        return Context(
            room=room, 
            event=message,
            command=command,
            args=args
        )

    @staticmethod
    def from_text(room: MatrixRoom, message: RoomMessageText):
        return Context(
            room=room,
            event=message
        )

