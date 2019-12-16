from flask import Blueprint, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config
from models import Product, Category

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

products_app = Blueprint('products_app', __name__)


@products_app.route('/category/<int:id>', endpoint='category')
def products_in_category(id=None):
    category = session.query(Category).filter(Category.id == id).first()
    products = session.query(Product).filter(Product.category_id == id)

    print(category)
    context = {
        'category': category,
        'products': products,
    }

    return render_template('products/products_in_category.html', **context)


@products_app.route('/<int:id>/', endpoint='product')
def product(id=None):
    product = session.query(Product).filter(Product.id == id).first()
    return render_template('products/detail.html', product=product)
