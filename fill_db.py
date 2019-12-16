import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Category, Vendor, Product
from config import Config
import random
from faker import Faker

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# clear database
session.query(Product).delete()
session.query(Category).delete()
session.query(Vendor).delete()
session.commit()


def add_models_to_db(base_model, models):
    for model in models:
        session.add(base_model(**model))
    session.commit()


def set_image_url(image_folder, name, ext='.jpg'):
    """
    :return: image url or "<image-folder>/no-name.jpg"
    """
    path = os.path.join(os.getcwd(), 'static', image_folder, "".join([str(name), ext]))
    if os.path.exists(path):
        return os.path.join(image_folder, "".join([str(name), ext]))
    return os.path.join(image_folder, "".join(['no-image', ext]))


PRODUCT_QTY = 30
CATEGORIES_QTY = 5
VENDORS_QTY = 5

fake = Faker()

categories = [{'name': fake.company()} for category in range(CATEGORIES_QTY)]
vendors = [{'name': fake.company()} for vendor in range(VENDORS_QTY)]
products = [
    {'category_id': random.randint(1, CATEGORIES_QTY),
     'vendor_id': random.randint(1, VENDORS_QTY),
     'name': fake.name(),
     'description': fake.text(),
     'image': set_image_url(Config.IMAGES_PATH, i),
     'price': random.randint(100, 1000),
     'is_active': True
     } for i in range(PRODUCT_QTY)
]

add_models_to_db(Category, categories)
add_models_to_db(Vendor, vendors)
add_models_to_db(Product, products)
