# Copyright (C) 2022-2023 AyiinXd <https://github.com/AyiinXd>

# This file is part of GeneratorPassword.

# GeneratorPassword is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GeneratorPassword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with GeneratorPassword.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import string

from random import choice
from typing import Dict, Optional, Union

from .storage import Storage
from .tools import Tools


class Generate(Tools):
    def __init__(
        self,
        name: str = None,
        space_symbol: str = None,
    ):
        super().__init__()
        self.name = name if name else 'generate'
        self._space = space_symbol if space_symbol else '-_='
        
        self.memory = Storage(name)
        self._string = string.ascii_letters
        self.loop = asyncio.get_event_loop_policy().get_event_loop()
        
        self._cache: dict = {}
        self.is_authorize = None
        self.start()

    def authorize(self):
        if self.memory.is_connected:
            self.memory.close()

        self.memory.connect()
