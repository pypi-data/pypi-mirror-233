from nio import SyncResponse, AsyncClient
import cryptography
import asyncio
import os

from nio.crypto import ENCRYPTION_ENABLED

from .callbacks import Callbacks
from .listener import Listener
from .filters import Filter
from .api import Api

from .utils import info, error

class Bot:

    def __init__(self, creds, prefix: str="!", selfbot: bool=False) -> None:
        self.prefix = prefix
        self.selfbot = selfbot
        self.creds = creds 

        self.api = Api(self.creds)
        self.listener = Listener(self)
        self.filter = Filter(self)
        self.async_client: AsyncClient = None
        self.callbacks: Callbacks = None

    async def main(self) -> None:
        """
        Implementation from:
        https://codeberg.org/imbev/simplematrixbotlib/src/branch/master/simplematrixbotlib/bot.py
        """
        try:
            self.creds.session_read_file()
        except cryptography.fernet.InvalidToken:
            print("Invalid Stored Token")
            print("Regenerating token from provided credentials")
            os.remove(self.creds._session_stored_file)
            self.creds.session_read_file()

        await self.api.login()

        self.async_client = self.api.async_client

        resp = await self.async_client.sync(full_state=False)  #Ignore prior messages

        if isinstance(resp, SyncResponse):
            info(
                f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})"
            )
            if ENCRYPTION_ENABLED:
                key = self.async_client.olm.account.identity_keys['ed25519']
                info(
                    f"This bot's public fingerprint (\"Session key\") for one-sided verification is: "
                    f"{' '.join([key[i:i+4] for i in range(0, len(key), 4)])}")

        self.creds.session_write_file()

        self.callbacks = Callbacks(self.async_client, self)
        await self.callbacks.setup()

        for action in self.listener._startup_registry:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def run(self) -> None:
        asyncio.run(self.main())

