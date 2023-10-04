import asyncio
import sys

from datetime import datetime
from typing import Union, BinaryIO, List, Optional, Callable

from fipper import Client, enums, types

from pyAyiin.exceptions import pyAyiinError


class Ayiin(Client):
    def __init__(
        self,
        name: str = None,
        api_id: int = None,
        api_hash: str = None,
        bot_token: str = None,
        session: str = None,
        device: str = None,
        memory: bool = None,
        plugin: dict = None,
    ):
        self.name = name
        self.api_id = int(api_id) if api_id else int(6)
        self.api_hash = str(api_hash) if api_hash else 'eb06d4abfb49dc3eeb1aeb98ae0f581e'
        self.bot_token = bot_token
        self.session = session
        self.device = str(device) if device else 'pyAyiin'
        self.memory = memory
        self.plugin = plugin
        super().__init__(
            name=self.name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token,
            session_string=self.session,
            device_model=self.device,
            in_memory=self.memory,
            plugins=self.plugin
        )

        self.bot = None
        self.ayiin = None
        self._dialog: list = []
        self._cache: dict = {}
        self.full_name: Optional[str] = None
        self.uid: Optional[int] = None
        self.client_type: Optional[str] = None
        self.lop = asyncio.get_event_loop()

    def __repr__(self):
        return "<AyiinClient: client: {}\nbot: {}\n>".format(self, self.bot)

    async def ayiin_start(self: 'Ayiin'):
        try:
            await self.start()
        except BaseException as e:
            raise pyAyiinError(e)
        me = await self.get_me()
        if me.is_bot:
            self.uid = me.id
            last_ = "" if not me.last_name else me.last_name
            self.full_name = f'{me.first_name} {last_}'
            self.client_type = 'bot'
        else:
            self.uid = me.id
            last_ = "" if not me.last_name else me.last_name
            self.full_name = f'{me.first_name} {last_}'
            self.client_type = 'client'
        print(f'{self.client_type.capitalize()} Succesfully Started {self.full_name}')

    async def ayiin_stop(self: 'Ayiin'):
        if self.is_connected:
            try:
                await self.stop()
            except BaseException as e:
                raise pyAyiinError(e)
        else:
            print("Client has not started.")

    async def get_chats(self, chat_id) -> 'types.Chat':
        return await self.get_chat(chat_id)

    async def get_users(self, peer: int) -> 'types.User':
        return await self.get_users(peer)

    async def send_msg(
        self: 'Ayiin',
        chat_id: Union[int, str],
        text: str = None,
        animation: Union[str, BinaryIO] = None,
        audio: Union[str, BinaryIO] = None,
        document: Union[str, BinaryIO] = None,
        emoji: Union[List[str], str] = None,
        message_id: Union[int, str] = None,
        photo: Union[str, BinaryIO] = None,
        sticker: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        voice: Union[str, BinaryIO] = None,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        reply_message: int = None,
        parse: Optional["enums.ParseMode"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> Optional['types.Message']:
        if animation:
            await self.send_animation(
                chat_id=chat_id,
                animation=animation,
                caption=text,
                reply_markup=markup,
                thumb=thumb,
                parse_mode=parse,
                reply_to_message_id=reply_message,
                protect_content=protect_content,
            )
            return
        if audio:
            await self.send_audio(
                chat_id=chat_id,
                audio=audio,
                caption=text,
                parse_mode=parse,
                reply_markup=markup,
                file_name=file_name,
                thumb=thumb,
                reply_to_message_id=reply_message,
                disable_notification=disable_notification,
            )
            return
        if document:
            await self.send_document(
                chat_id=chat_id,
                document=document,
                caption=text,
                reply_markup=markup,
                thumb=thumb,
                parse_mode=parse,
                file_name=file_name,
                protect_content=protect_content,
                reply_to_message_id=reply_message
            )
            return
        if photo:
            await self.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=markup,
                parse_mode=parse,
                reply_to_message_id=reply_message,
                protect_content=protect_content,
                disable_notification=disable_notification
            )
            return
        if sticker:
            await self.send_sticker(
                chat_id=chat_id,
                sticker=sticker,
                disable_notification=disable_notification,
                reply_markup=markup,
                reply_to_message_id=reply_message,
                protect_content=protect_content
            )
            return
        if video:
            await self.send_video(
                chat_id=chat_id,
                video=video,
                caption=text,
                reply_markup=markup,
                parse_mode=parse,
                thumb=thumb,
                protect_content=protect_content,
                disable_notification=disable_notification
            )
            return
        if voice:
            await self.send_voice(
                chat_id=chat_id,
                voice=voice,
                caption=text,
                reply_markup=markup,
                reply_to_message_id=reply_message,
                parse_mode=parse,
                disable_notification=disable_notification,
                protect_content=protect_content
            )
            return
        if emoji:
            if isinstance(emoji, list):
                for i in emoji:
                    reaction = i
            if isinstance(emoji, str):
                reaction = emoji
            await self.send_reaction(
                chat_id=chat_id,
                message_id=message_id,
                emoji=reaction
            )
            return
        else:
            await self.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse,
                reply_markup=markup,
                reply_to_message_id=reply_message,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                protect_content=protect_content
            )
            return
