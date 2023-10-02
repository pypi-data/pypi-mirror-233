from nio import SyncResponse, AsyncClient
import asyncio
import json

from .callbacks import Callbacks
from .listener import Listener
from .api import Api

from .utils import info, error

class Bot:

    def __init__(self, creds, prefix: str="!") -> None:
        self.prefix = prefix
        
        if type(creds) == str:
            self.creds = json.load(open(creds, mode="r"))
        elif type(creds) == dict:
            self.creds = creds
        else:
            error("Credits object has incorrect value!")
            raise ValueError("Credits object has incorrect value!")

        self.api = Api(self.creds)
        self.listener = Listener(self)
        self.async_client: AsyncClient = None
        self.callbacks: Callbacks = None

    async def main(self) -> None:
        client = await self.api.login()
        if client is None: return
        self.async_client = client
        
        resp = await self.async_client.sync(full_state=False)

        if isinstance(resp, SyncResponse):
            info("Connected!")

        self.callbacks = Callbacks(self.async_client, self)
        await self.callbacks.setup()

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def run(self) -> None:
        asyncio.run(self.main())

