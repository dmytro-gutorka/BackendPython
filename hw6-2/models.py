from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, func, Column, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
	pass


db = SQLAlchemy(model_class=Base)


class ItemStatus(PyEnum):
	RENTED = 'Rented'
	MAINTENANCE = 'Maintenance'
	AVAILABLE = 'Available'
	ON_HOLD = 'On_hold'


class User(db.Model):
	__tablename__ = 'user'

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str]
	first_name: Mapped[str] = mapped_column(String(30))
	last_name: Mapped[str] = mapped_column(String(30))
	photo: Mapped[Optional[str]]


# class UserProfile(db.Model):
# 	pass


class Item(db.Model):
	__tablename__ = 'item'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(50))
	photo: Mapped[str]
	status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.AVAILABLE)
	price_per_hour: Mapped[float]
	price_per_day: Mapped[float]
	price_per_week: Mapped[float]
	price_per_month: Mapped[float]
	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Contract(db.Model):
	__tablename__ = 'contract'

	id: Mapped[int] = mapped_column(primary_key=True)
	description: Mapped[Optional[str]] = mapped_column(String(50), default='')
	start_date: Mapped[datetime]
	end_date: Mapped[datetime]
	renter_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))


class Feedback(db.Model):
	__tablename__ = 'feedback'

	id: Mapped[int] = mapped_column(primary_key=True)
	from_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
	to_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
	contract: Mapped[int] = mapped_column(ForeignKey('contract.id'))
	description: Mapped[str] = mapped_column(String(500))


class Favourite(db.Model):
	__tablename__ = 'favourite'

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))


class SearchHistory(db.Model):
	__tablename__ = 'search_history'

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	searched_at: Mapped[datetime] = mapped_column(insert_default=func.now())
