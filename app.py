from flask import Flask, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import config
from product_views import products_app
from main_view import main_page_app
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
app.register_blueprint(main_page_app, url_prefix='/')

app.run('localhost', 8080, debug=True)
