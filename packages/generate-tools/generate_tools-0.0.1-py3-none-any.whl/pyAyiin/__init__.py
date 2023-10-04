# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio
import logging
import sys
import time
from aiohttp import ClientSession

from .telethon import AyiinClient
from .pyrogram import Ayiin
from .xd import GenSession


# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pyAyiin").setLevel(logging.INFO)
logging.getLogger("pytgcalls").setLevel(logging.INFO)
logging.getLogger("fipper").setLevel(logging.ERROR)
logging.getLogger("fipper.client").setLevel(logging.ERROR)
logging.getLogger("fipper.session.auth").setLevel(logging.ERROR)
logging.getLogger("fipper.session.session").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.client").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.auth").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.INFO)


logs = logging.getLogger(__name__)


__copyright__ = "Copyright (C) 2022-present AyiinXd <https://github.com/AyiinXd>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.0.1"


DEVS = [
    607067484, # Ayiin
    997461844, #Ayang_Ayiin
    2130526178, # Alfa
]

BLACKLIST_CHAT = [
    -1001797285258,  # AyiinChatsNew
    -1001675396283,  # AyiinXdSupport
    -1001473548283,  # SharingUserbot
]

GCAST_BLACKLIST = [
    -1001797285258,  # AyiinChatsNew
    -1001675396283,  # AyiinXdSupport
    -1001473548283,  # SharingUserbot
    -1001433238829,  # TedeSupport
    -1001476936696,  # AnosSupport
    -1001327032795,  # UltroidSupport
    -1001294181499,  # UserBotIndo
    -1001419516987,  # VeezSupportGroup
    -1001459812644,  # GeezSupportGroup
    -1001296934585,  # X-PROJECT BOT
    -1001481357570,  # UsergeOnTopic
    -1001459701099,  # CatUserbotSupport
    -1001109837870,  # TelegramBotIndonesia
    -1001752592753,  # Skyzusupport
    -1001788983303,  # KayzuSupport
    -1001380293847,  # NastySupport
    -1001692751821,  # RamSupport
    -1001267233272,  # PocongUserbot
    -1001500063792,  # Trident
    -1001687155877,  # CilikSupport
    -1001578091827,  # PrimeSupport
    -1001704645461,  # Jamet No Support
    -1001662510083,  # MutualanDestra
    -1001347414136,  # ArunaMutualan
    -1001572486389,  # PluviaMusicGroup
    -1001608701614,  # UputtSupport
    -1001864253073,  # RitoSupport
]
