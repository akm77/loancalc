from charset_normalizer.md import Optional
from sqlalchemy import Result
from sqlalchemy.dialects.sqlite import insert, Insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.models.base import User


def get_upsert_user_query(values) -> Insert:
    insert_statement = insert(User).values(values)
    update_statement = insert_statement.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(is_bot=insert_statement.excluded.is_bot,
                  first_name=insert_statement.excluded.first_name,
                  last_name=insert_statement.excluded.last_name,
                  username=insert_statement.excluded.username,
                  language_code=insert_statement.excluded.language_code,
                  is_premium=insert_statement.excluded.is_premium)).returning(User)
    return update_statement


async def upsert_user_from_middleware(session: async_sessionmaker, user: User) -> Optional[User]:
    # id: Mapped[int] = mapped_colu-mn(primary_key=True)
    # is_bot: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    # first_name: Mapped[str] = mapped_column(nullable=False)
    # last_name: Mapped[str] = mapped_column(nullable=True)
    # username: Mapped[str] = mapped_column(nullable=True)
    # lang_code: Mapped[str] = mapped_column(nullable=True, server_default=text("ru_RU"))
    # is_premium: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    # role: Mapped[str] = mapped_column(String(length=100), server_default=text("user"))
    async with session() as session:
        result: Result = await session.execute(get_upsert_user_query({"id": user.id,
                                                                      "is_bot": user.is_bot,
                                                                      "first_name": user.first_name,
                                                                      "last_name": user.last_name,
                                                                      "username": user.username,
                                                                      "language_code": user.language_code,
                                                                      "is_premium": user.is_premium if user.is_premium
                                                                      else False}))
        await session.commit()
        return result.scalars().one_or_none()


