from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True)


db = SQLAlchemy(model_class=Base)


class ItemStatus(PyEnum):
	RENTED = 'Rented'
	MAINTENANCE = 'Maintenance'
	AVAILABLE = 'Available'
	ON_HOLD = 'On_hold'


class User(db.Model):
	__tablename__ = 'user'

	username: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str]
	first_name: Mapped[str] = mapped_column(String(30))
	last_name: Mapped[str] = mapped_column(String(30))
	photo: Mapped[Optional[str]]

	items: Mapped[List['Item']] = relationship(back_populates='user', cascade='all, delete')


class Item(db.Model):
	__tablename__ = 'item'

	name: Mapped[str] = mapped_column(String(50))
	description: Mapped[Optional[str]] = mapped_column(String(250), default='')
	photo: Mapped[Optional[str]]  # Optional for now
	status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.AVAILABLE)
	price_per_hour: Mapped[float]
	price_per_day: Mapped[float]
	price_per_week: Mapped[float]

	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

	user: Mapped['User'] = relationship(back_populates='items')
	contract: Mapped[Optional['Contract']] = relationship(back_populates='item', uselist=True)


class Contract(db.Model):
	__tablename__ = 'contract'

	description: Mapped[Optional[str]] = mapped_column(String(50), default='')
	start_date: Mapped[datetime]
	end_date: Mapped[datetime]

	renter_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	host_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), unique=True)

	item: Mapped['Item'] = relationship(back_populates='contract')


class Feedback(db.Model):
	__tablename__ = 'feedback'

	contract: Mapped[int] = mapped_column(ForeignKey('contract.id'))
	description: Mapped[str] = mapped_column(String(500))

	from_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
	to_user: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Favourite(db.Model):
	__tablename__ = 'favourite'

	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))


# class SearchHistory(db.Model):
# 	__tablename__ = 'search_history'
#
# 	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
# 	searched_at: Mapped[datetime] = mapped_column(insert_default=func.now())
#   TODO-1: Store search history in sessions ?


