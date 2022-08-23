from __future__ import annotations

from typing import Any

import aiohttp
import crescent

from mcodingbot.config import CONFIG


class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=CONFIG.discord_token)

        self.plugins.load_folder("mcodingbot.plugins")
        self.plugins.load_folder("mcodingbot.tasks")

        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            raise AttributeError("Session has not been set yet.")
        return self._session

    async def start(self, *args: Any, **kwargs: Any) -> None:
        self._session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)

    async def join(self, *args: Any, **kwargs: Any) -> None:
        await super().join(*args, **kwargs)
        if self._session and not self._session.closed:
            await self._session.close()
