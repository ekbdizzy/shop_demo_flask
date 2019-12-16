from flask import Flask, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import config
from product_views import products_app
from models import Vendor, Category, Product

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)
db.init_app(app)

engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

admin = Admin(app, name='Flask Shop', template_mode='bootstrap3')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Vendor, db.session))
admin.add_view(ModelView(Product, db.session))

app.register_blueprint(products_app, url_prefix='/products')


@app.route('/', endpoint='main')
def index():
    categories = session.query(Category).all()

    # get first 3 product of categories for preview
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

    page = render_template('index.html', **context)
    return page


if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)
