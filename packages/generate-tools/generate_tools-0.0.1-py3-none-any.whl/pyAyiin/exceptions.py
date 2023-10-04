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

"""
Exceptions which can be raised by py-Ayiin Itself.
"""


class pyAyiinError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class InvalidMtProtoClient(Exception):
    """You set an invalid MtProto client, raised by
    :meth:`~pyAyiin.Ayiin`
    """

    def __init__(self):
        super().__init__(
            'Invalid MtProto Client',
        )

class FipperMissingError(ImportError):
    ...

class TelethonMissingError(ImportError):
    ...

class DependencyMissingError(ImportError):
    ...

class RunningAsFunctionLibError(pyAyiinError):
    ...

class SpamFailed(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class DownloadFailed(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class DelAllFailed(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class FFmpegReturnCodeError(Exception):
    def __init__(self, error: str):
        super().__init__(error)
