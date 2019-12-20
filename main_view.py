from flask import Blueprint, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config
from models import Product, Category

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

main_page_app = Blueprint('main_page_app', __name__)


@main_page_app.route('', endpoint='')
def main_page_view():
    categories = session.query(Category).all()

    # get first 4 products of categories for preview
    preview_products_in_category = {}
    for category in categories:
        products_in_category = session.query(Product).join(Category).filter(Category.id == category.id).all()
        if len(products_in_category) > 3:
            preview_products_in_category[category] = [product for product in products_in_category[:4]]
        else:
            preview_products_in_category[category] = [product for product in products_in_category]

    context = {
        'preview_products_in_category': preview_products_in_category,
    }

    return render_template('index.html', **context)
