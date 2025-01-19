from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True)


db = SQLAlchemy(model_class=Base)


class ItemStatus(PyEnum):
	RENTED = 'Rented'
	MAINTENANCE = 'Maintenance'
	AVAILABLE = 'Available'
	ON_HOLD = 'On_Hold'


class User(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str]
	first_name: Mapped[str] = mapped_column(String(30))
	last_name: Mapped[str] = mapped_column(String(30))
	phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
	birthday: Mapped[datetime] = mapped_column(String(15))
	photo: Mapped[Optional[str]]

	items: Mapped[List['Item']] = relationship(back_populates='user', cascade='all, delete')


class Item(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(50))
	description: Mapped[Optional[str]] = mapped_column(String(250), default='No description yet')
	photo: Mapped[Optional[str]]
	status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.AVAILABLE)
	price_per_hour: Mapped[float]
	price_per_day: Mapped[float]
	price_per_week: Mapped[float]

	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

	user: Mapped['User'] = relationship(back_populates='items')
	contract: Mapped[Optional['Contract']] = relationship(back_populates='item', uselist=True)


class Contract(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	description: Mapped[Optional[str]] = mapped_column(String(50), default='')
	start_date: Mapped[datetime.date] = mapped_column(Date)
	end_date: Mapped[datetime.date] = mapped_column(Date)

	renter_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	host_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), unique=True)

	item: Mapped['Item'] = relationship(back_populates='contract')


class Feedback(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	contract: Mapped[int] = mapped_column(ForeignKey('contract.id'))
	description: Mapped[str] = mapped_column(String(500))

	from_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
	to_user: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Favourite(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))