import os
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config import Config

Base = declarative_base()


class Vendor(Base):
    __tablename__ = 'vendor'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)

    products = relationship("Product", back_populates='vendors', lazy="joined")

    def __repr__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)

    products = relationship("Product", back_populates='categories', lazy="joined")

    def __repr__(self):
        return self.name


class Product(Base):
    __tablename__ = 'product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('category.id'), nullable=False)
    vendor_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('vendor.id'), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL(10, 2))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    vendors = relationship('Vendor', back_populates='products', lazy="joined")
    categories = relationship('Category', back_populates='products', lazy="joined")

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
