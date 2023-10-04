import asyncio
from typing import Optional, Union, Type

from telethon.client import TelegramClient
from telethon.tl.types import User
from telethon.network import Connection, ConnectionTcpFull, ConnectionTcpAbridged
from telethon.utils import get_display_name

from pyAyiin.exceptions import pyAyiinError

from ..ayiin import Decorator

class AyiinClient(TelegramClient, Decorator):
    def __init__(
        self,
        session: str = None,
        api_id: int = None,
        api_hash: str = None,
        bot_token: str = None,
        connection: 'Type[Connection]' = ConnectionTcpFull,
        connection_retries: int = None,
        device: str = None,
    ):
        self.api_id = int(api_id) if api_id is not None else 6
        self.api_hash = str(api_hash) if api_hash else 'eb06d4abfb49dc3eeb1aeb98ae0f581e'
        self.session = session
        self.bot_token = bot_token
        self.connection = connection if connection is not None else ConnectionTcpAbridged
        self.connection_retries = connection_retries if connection_retries else int(5)
        self.device = str(device) if device else 'pyAyiin'
        super().__init__(
            session=self.session,
            api_id=self.api_id,
            api_hash=self.api_hash,
            connection=self.connection,
            auto_reconnect=True,
            connection_retries=self.connection_retries,
            device_model=self.device
        )

        self.bot = None
        self.ayiin = None
        self.me: Optional[User] = None
        self._bl_chat: list = []
        self._dialog: list = []
        self._cache: dict = {}
        self._ubot: list = []
        self.sudoer: list = []
        self.full_name: Optional[str] = None
        self.uid: Optional[int] = None
        self.client_type: Optional[str] = None
        self.lop = asyncio.get_event_loop()

    async def ayiin_start(self: 'AyiinClient'):
        try:
            if self.bot_token:
                await self.start(bot_token=self.bot_token)
            else:
                await self.start()
                self._ubot.append(self)
        except BaseException as e:
            raise pyAyiinError(e)
        self.me = await self.get_me()
        if await self.is_bot():
            self.uid = self.me.id
            last_ = "" if not self.me.last_name else self.me.last_name
            self.full_name = f'{self.me.first_name} {last_}'
            self.client_type = 'bot'
        else:
            self.uid = self.me.id
            last_ = "" if not self.me.last_name else self.me.last_name
            self.full_name = f'{self.me.first_name} {last_}'
            self.client_type = 'client'
        print(f'{self.client_type.capitalize()} Succesfully Started {self.full_name}')

    async def send_msg(self, chat_id, text):
        return await self.send_message(chat_id, message=text)

    async def get_msg(self, chat_id, msg_id):
        return await self.get_messages(chat_id, msg_id)

    async def get_chats(self, chat_id):
        return await self.get_entity(chat_id)

    async def get_users(self, chat_id):
        return await self.get_users(chat_id)
