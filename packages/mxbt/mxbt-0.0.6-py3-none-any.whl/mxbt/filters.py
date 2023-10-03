from nio import MatrixRoom, RoomMessageText
from .match import Match
from .context import Context

class Filter:

    def __init__(self, bot) -> None:
        self._bot = bot

    def from_users(self, users: list):
        """
        from_users event filter

        filter params:
        ----------------
        users: list[str] - list of user_id, who is accepted to send event

        func params:
        --------------
        room: MatrixRoom,
        event: Event

        or 

        ctx: Context
        """
        def wrapper(func):
            async def command_func(*args) -> None:
                if len(args) == 1 and type(args[0]) == Context:
                    ctx = args[0]
                    match = Match(ctx.room, ctx.event, self._bot)
                    if match.is_from_users(users):
                        await func(ctx)
                else:
                    room, message = args[0:2]
                    match = Match(room, message, self._bot)
                    if match.is_from_users(users):
                        await func(room, message)
            return command_func
        return wrapper


