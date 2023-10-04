# Credits: @mrconfused
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import logging
import inspect
import re
from pathlib import Path

from telethon import events
from telethon.errors import (
    AlreadyInConversationError,
    BotInlineDisabledError,
    BotResponseTimeoutError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

import pyAyiin
from ._wrappers import eod, eor


LOGS = logging.getLogger(__name__)


class Decorator:
    def ayiin_cmd(
        self: 'pyAyiin.AyiinClient',
        pattern: str = None,
        allow_sudo: bool = True,
        group_only: bool = False,
        admins_only: bool = False,
        private_only: bool = False,
        disable_edited: bool = False,
        forword=False,
        command: str = None,
        **args,
    ):
        args["func"] = lambda e: e.via_bot_id is None
        stack = inspect.stack()
        previous_stack_frame = stack[1]
        file_test = Path(previous_stack_frame.filename)
        file_test = file_test.stem.replace(".py", "")

        if "disable_edited" in args:
            del args["disable_edited"]

        args["blacklist_chats"] = True
        black_list_chats = self._bl_chat
        if len(black_list_chats) > 0:
            args["chats"] = black_list_chats

        def decorator(func):
            async def wrapper(event):
                chat = event.chat
                if admins_only:
                    if event.is_private:
                        return await eor(
                            event,
                            "**Perintah ini hanya bisa digunakan di grup.**",
                            time=10
                        )
                    if not (chat.admin_rights or chat.creator):
                        return await eor(
                            event,
                            f"**Maaf anda bukan admin di {chat.title}**",
                            time=10
                        )
                if group_only and not event.is_group:
                    return await eor(
                        event,
                        "**Perintah ini hanya bisa digunakan di grup.**",
                        time=10
                    )
                if private_only and not event.is_private:
                    return await eor(
                        event,
                        "**Perintah ini hanya bisa digunakan di private chat.**",
                        time=10
                    )
                try:
                    await func(event)
                # Credits: @mrismanaziz
                # FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
                # t.me/SharingUserbot & t.me/Lunatic0de
                except MessageNotModifiedError as er:
                    LOGS.error(er)
                except MessageIdInvalidError as er:
                    LOGS.error(er)
                except BotInlineDisabledError:
                    await eor(
                        event,
                        "**Silahkan aktifkan mode Inline untuk bot**",
                        time=10
                    )
                except ChatSendStickersForbiddenError:
                    await eor(
                        event,
                        "**Tidak dapat mengirim stiker di obrolan ini**",
                        time=10
                    )
                except BotResponseTimeoutError:
                    await eod(
                        event,
                        "**The bot didnt answer to your query in time**"
                    )
                except ChatSendMediaForbiddenError:
                    await eor(
                        event,
                        "**Tidak dapat mengirim media dalam obrolan ini**",
                        time=10
                    )
                except AlreadyInConversationError:
                    await eod(
                        event,
                        "**Percakapan sudah terjadi dengan obrolan yang diberikan. coba lagi setelah beberapa waktu.**",
                    )
                except ChatSendInlineForbiddenError:
                    await eor(
                        event,
                        "**Tidak dapat mengirim pesan inline dalam obrolan ini.**",
                        time=10,
                    )
                except FloodWaitError as e:
                    LOGS.info(
                        f"Telah Terjadi flood wait error tunggu {e.seconds} detik dan coba lagi"
                    )
                    await event.delete()
                    await asyncio.sleep(e.seconds + 5)
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except BaseException as e:
                    LOGS.exception(e)

            for ubot in self._ubot:
                if not disable_edited:
                    ubot.add_event_handler(
                        wrapper, events.MessageEdited(
                            **args,
                            outgoing=True,
                            pattern=pattern
                        )
                    )
                ubot.add_event_handler(
                    wrapper, events.NewMessage(
                        **args,
                        outgoing=True,
                        pattern=pattern
                    )
                )
                if allow_sudo:
                    if not disable_edited:
                        ubot.add_event_handler(
                            wrapper,
                            events.MessageEdited(
                                **args,
                                from_users=self.sudoer,
                                pattern=pattern
                            ),
                        )
                    ubot.add_event_handler(
                        wrapper,
                        events.NewMessage(
                            **args,
                            from_users=self.sudoer,
                            pattern=pattern
                        ),
                    )
            return wrapper

        return decorator


    def ayiin_handler(
        self: 'pyAyiin.AyiinClient',
        **args,
    ):
        def decorator(func):
            for ub in self._ubot:
                ub.add_event_handler(func, events.NewMessage(**args))
            return func

        return decorator


    def asst_cmd(self: 'pyAyiin.AyiinClient', **args):
        pattern = args.get("pattern", None)
        r_pattern = r"^[/!]"
        if pattern is not None and not pattern.startswith("(?i)"):
            args["pattern"] = "(?i)" + pattern
        args["pattern"] = pattern.replace("^/", r_pattern, 1)

        def decorator(func):
            if self.bot:
                self.bot.add_event_handler(func, events.NewMessage(**args))
            return func

        return decorator


    def chataction(self: 'pyAyiin.AyiinClient', **args):
        def decorator(func):
            for Ayiin in self._ubot:
                Ayiin.add_event_handler(func, events.ChatAction(**args))
            return func

        return decorator


    def callback(self: 'pyAyiin.AyiinClient', **args):
        def decorator(func):
            if self.bot:
                self.bot.add_event_handler(func, events.CallbackQuery(**args))
            return func

        return decorator
