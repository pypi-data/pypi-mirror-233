from nio import AsyncClient, LoginResponse, OlmUnverifiedDeviceError, UploadResponse 
from typing import List 
from PIL import Image
import aiofiles.os
import mimetypes
import markdown
import os

from .utils import info, error

class Api:

    def __init__(self, creds) -> None:
        self.creds = creds
        self.async_client: AsyncClient = None

    async def login(self) -> AsyncClient | None:
        self.async_client = AsyncClient(
            homeserver=self.creds['homeserver'], 
            user=self.creds['user_id'], 
        )
        resp = await self.async_client.login(
            password=self.creds['password'],
            device_name='mxbt'
        )

        # check that we logged in successfully
        if isinstance(resp, LoginResponse):
            info(f"Logged in as @{self.creds['user_id']}.")
            #self.config.write_credits_to_file(resp, homeserver)
        else:
            #print(f'homeserver = "{homeserver}"; user = "{user_id}"')
            error(f"Failed to log in: {resp}")
            exit(1)

        return self.async_client

    async def _send_room(self,
                         room_id: str,
                         content: dict,
                         message_type: str = "m.room.message",
                         ignore_unverified_devices: bool = None) -> None:
        """
        Send a custom event in a Matrix room.

        Parameters
        -----------
        room_id : str
            The room id of the destination of the message.

        content : dict
            The content block of the event to be sent.

        message_type : str, optional
            The type of event to send, default m.room.message.

        ignore_unverified_devices : bool, optional
            Whether to ignore that devices are not verified and send the
            message to them regardless on a per-message basis.
        """

        try:
            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices)
        except OlmUnverifiedDeviceError as e:
            # print(str(e))
            error(
                "Message could not be sent. "
                "Set ignore_unverified_devices = True to allow sending to unverified devices."
            )
            error("Automatically blacklisting the following devices:")
            for user in self.async_client.rooms[room_id].users:
                if self.async_client.olm is None: break
                unverified: List[str] = list()
                for device_id, device in self.async_client.olm.device_store[
                    user].items():
                    if not (self.async_client.olm.is_device_verified(device) or
                            self.async_client.olm.is_device_blacklisted(device)
                    ):
                        self.async_client.olm.blacklist_device(device)
                        unverified.append(device_id)
                if len(unverified) > 0:
                    info(f"\tUser {user}: {', '.join(unverified)}")

            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices)

    async def send_text(self, room_id: str, body: str,
                        msgtype: str="m.text",
                        reply_to: str="", edit_id: str="") -> None:
        content: dict[str, str | dict] = {
            "msgtype" : msgtype,
            "body" : body,
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }
            
        await self._send_room(room_id=room_id, content=content)

    async def send_markdown(self, room_id: str, body: str,
                        msgtype: str="m.text",
                        reply_to: str="", edit_id: str="") -> None:
        content: dict[str, str | dict] = {
            "msgtype" : msgtype,
            "body" : body,
            "format" : "org.matrix.custom.html",
            "formatted_body" : markdown.markdown(body, extensions=['fenced_code', 'nl2br'])
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }
            
        await self._send_room(room_id=room_id, content=content)

    async def send_reaction(self, room_id: str, event_id: str, key: str) -> None:
        await self._send_room(
            room_id=room_id,
            content={
                "m.relates_to": {
                    "event_id": event_id,
                    "key": key,
                    "rel_type": "m.annotation"
                }
            },
            message_type="m.reaction"
        )

    async def send_image(self, room_id: str, 
                         image_filepath: str, 
                         reply_to: str="", edit_id: str="") -> None:
        mime_type = mimetypes.guess_type(image_filepath)[0]
        if mime_type is None: return

        image = Image.open(image_filepath)
        (width, height) = image.size

        file_stat = await aiofiles.os.stat(image_filepath)
        async with aiofiles.open(image_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(image_filepath),
                filesize=file_stat.st_size)
        if isinstance(resp, UploadResponse):
            pass  # Successful upload
        else:
            info(f"Failed Upload Response: {resp}")
            return

        content = {
            "body": os.path.basename(image_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None,
                "w": width,
                "h": height,
                "thumbnail_url": None
            },
            "msgtype": "m.image",
            "url": resp.content_uri
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }

        try:
            await self._send_room(room_id=room_id, content=content)
        except:
            error(f"Failed to send image file {image_filepath}")

    async def send_video(self, room_id: str,
                         video_filepath: str,
                         reply_to: str="", edit_id: str="") -> None:
        """
        Send a video message in a Matrix room.

        Parameters
        ----------
        room_id : str
            The room id of the destination of the message.

        video_filepath : str
            The path to the video on your machine.
        """

        mime_type = mimetypes.guess_type(video_filepath)[0]

        file_stat = await aiofiles.os.stat(video_filepath)
        async with aiofiles.open(video_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(video_filepath),
                filesize=file_stat.st_size)

        if isinstance(resp, UploadResponse):
            pass  # Successful upload
        else:
            error(f"Failed Upload Response: {resp}")
            return

        content = {
            "body": os.path.basename(video_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None
            },
            "msgtype": "m.video",
            "url": resp.content_uri
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }

        try:
            await self._send_room(room_id=room_id, content=content)
        except:
            error(f"Failed to send video file {video_filepath}")

