from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Optional, Annotated
from datetime import datetime, timezone

import enum

pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                               onupdate=datetime.now(timezone.utc))]


class Base(DeclarativeBase):

	repr_col_numb = 3
	repr_col_name = tuple()

	def __repr__(self):
		columns = [f"{col}={getattr(self, col)}" for inx, col in enumerate(self.__table__.columns.keys())
		           if col in self.repr_col_name or self.repr_col_numb > inx]
		return f"<{self.__class__.__name__}: {', '.join(columns)}>"


class Workload(enum.Enum):
	parttime = "parttime"
	fulltime = "fulltime"


class Workers(Base):
	__tablename__ = 'workers'

	repr_col_numb = 2

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str]


class Resumes(Base):
	__tablename__ = 'resumes'

	id: Mapped[int] = mapped_column(primary_key=True)
	worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))
	title: Mapped[str] = mapped_column(String(256))
	compensation: Mapped[Optional[int]] # instead of Optional[int] also can be user "int | None" or mapped_column(nullable=True)
	workload: Mapped[Workload]
	created_at: Mapped[created_at]
	updated_at: Mapped[updated_at]


