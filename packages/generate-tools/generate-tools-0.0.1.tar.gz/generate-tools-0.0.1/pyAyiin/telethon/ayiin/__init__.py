from ._wrappers import eod, eor, _try_delete
from .decorator import Decorator
from .events import Events
from .misc import Misc_


class AyiinMethod(
    Decorator,
    Events,
    Misc_,
):
    pass
