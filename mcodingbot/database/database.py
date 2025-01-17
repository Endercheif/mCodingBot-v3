from __future__ import annotations

import logging
from typing import TypeVar

import apgorm

from mcodingbot.config import CONFIG
from mcodingbot.database.models import Highlight, User, UserHighlight

_LOGGER = logging.getLogger(__name__)
_SELF = TypeVar("_SELF", bound="Database")


class Database(apgorm.Database):
    users = User
    user_highlights = UserHighlight
    highlights = Highlight

    @classmethod
    async def create(cls: type[_SELF]) -> _SELF:
        db = cls("mcodingbot/database/migrations")
        await db.connect(
            host="localhost",
            database="mcodingbot",
            user="mcodingbot",
            password=CONFIG.db_password,
        )
        if db.must_create_migrations():
            _LOGGER.info("Creating migrations...")
            db.create_migrations()
        if await db.must_apply_migrations():
            _LOGGER.info("Applying migrations...")
            await db.apply_migrations()

        return db
