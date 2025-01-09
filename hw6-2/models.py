import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Enum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
	pass


class ItemStatus(enum.Enum):
	rented = 'rented'
	maintenance = 'maintenance'
	available = 'available'
	on_hold = 'on_hold'


class User(Base):
	__tablename__ = 'user'

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str]
	first_name: Mapped[str] = mapped_column(String(30))
	last_name: Mapped[str] = mapped_column(String(30))
	photo: Optional[str]


class Item(Base):
	__tablename__ = 'item'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(50))
	photo: Mapped[str]
	status: [ItemStatus]
	price_per_hour: Mapped[float]
	price_per_day: Mapped[float]
	price_per_week: Mapped[float]
	price_per_month: Mapped[float]
	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Contract(Base):
	__tablename__ = 'contract'

	id: Mapped[int] = mapped_column(primary_key=True)
	description: Optional[str] = mapped_column(String(50), default='')
	start_date: Mapped[datetime]
	end_date: Mapped[datetime]
	renter_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))


class Feedback(Base):
	__tablename__ = 'feedback'

	id: Mapped[int] = mapped_column(primary_key=True)
	from_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
	to_user:  Mapped[int] = mapped_column(ForeignKey('user.id'))
	contract: Mapped[int] = mapped_column(ForeignKey('contract.id'))
	description: Mapped[str] = mapped_column(String(500))


class Favourite(Base):
	__tablename__ = 'favourite'

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))


class SearchHistory(Base):
	__tablename__ = 'search_history'

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	searched_at: Mapped[datetime] = mapped_column(insert_default=func.now())