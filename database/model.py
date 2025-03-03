# yuklamalar
from sqlalchemy import String, Integer, DateTime , ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from datetime import datetime

db_url = "sqlite+aiosqlite:///classmaster.db"

engine = create_async_engine(url=db_url)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    fam: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    usertype: Mapped[str] = mapped_column(String, default="user") #admin, user
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Test(Base):
    __tablename__="tests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String)
    code_test: Mapped[str] = mapped_column(String)
    answers: Mapped[str] = mapped_column(String)
    test_holati: Mapped[str] = mapped_column(String, default="yaratildi") #yaratilid, ,ish_jarayonida yakunlandi
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    

class UserAnswers(Base):
    __tablename__="useranswers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey("tests.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    true_answers: Mapped[int] = mapped_column(Integer)
    false_answers: Mapped[int] = mapped_column(Integer)
    user_answers: Mapped[str] = mapped_column(String)
    score: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
async def main_db_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)