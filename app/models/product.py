from flask import current_app
from sqlalchemy import Column, Integer, String, SmallInteger, Float, ForeignKey, orm, or_, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Product(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    image1 = Column(String(100))
    image2 = Column(String(100))
    image3 = Column(String(100))
    title = Column(String(100), nullable=False)
    currentPrice = Column(Float)
    originalPrice = Column(Float)
    description = Column(String(1000))
    address = Column(String(100))
    kind = Column(Integer)
    degree = Column(SmallInteger)
    state = Column(String(1))

    def __init__(self):
        if self.create_time is None:
            super(Product, self).__init__()

    def keys(self):
        return ['id', 'user_id', 'image1', 'image2',
                'image3', 'title', 'currentPrice',
                'originalPrice', 'description', 'address',
                'kind', 'degree', 'state', 'create_datetime']

    @staticmethod
    def add(title, currentPrice, originalPrice, description, address, kind, degree, state, user_id):
        """

        :param title:
        :param currentPrice:
        :param originalPrice:
        :param description:
        :param address:
        :param kind:
        :param degree:
        :param state:
        :param user_id:
        :return:
        """
        with db.auto_commit():
            product = Product()
            product = Product.fill_information(address, currentPrice, degree,
                                               description, kind, originalPrice,
                                               product, state,
                                               title, user_id)

            db.session.add(product)

    @staticmethod
    def renew(product_id, title, currentPrice, originalPrice, description, address, kind, degree, state, user_id):
        """

        :param product_id:
        :param title:
        :param currentPrice:
        :param originalPrice:
        :param description:
        :param address:
        :param kind:
        :param degree:
        :param state:
        :param user_id:
        :return:
        """
        with db.auto_commit():
            Product.fill_information(address, currentPrice, degree,
                                     description, kind, originalPrice,
                                     Product.verify_user_product(user_id, product_id),
                                     state, title, user_id)

    @staticmethod
    def fill_information(address, currentPrice, degree, description, kind, originalPrice, product, state, title,
                         user_id):
        """

        :param address:
        :param currentPrice:
        :param degree:
        :param description:
        :param kind:
        :param originalPrice:
        :param product:
        :param state:
        :param title:
        :param user_id:
        :return:
        """
        product.title = title
        product.currentPrice = currentPrice
        product.originalPrice = originalPrice
        product.description = description
        product.address = address
        product.kind = kind
        product.degree = degree
        product.state = state
        product.user_id = user_id
        return product

    @staticmethod
    def verify_user_product(user_id, product_id):
        return Product.query.filter_by(id=product_id, user_id=user_id).first_or_404()

    @staticmethod
    def get_user_products(user_id, begin, page):
        return Product.query.filter_by(user_id=user_id).limit(page).offset(begin).all()

    @staticmethod
    def get_products_filter(form):
        page = current_app.config['PAGE']
        product_filter = Product().query.filter(Product.status == 1)
        product_filter = Product().search_by_kind(product_filter, form.kind.data)
        product_filter = Product().search_by_key(product_filter, form.key.data)
        product_filter = Product().search_orderby_price(product_filter, form.price.data)
        product_filter = Product().search_orderby_time(product_filter, form.time.data)
        product_filter = product_filter.limit(page).offset(page * form.page.data)
        return product_filter

    @staticmethod
    def search_by_key(product_filter, key):
        if key:
            q = '%' + key + '%'
            return product_filter.filter(or_(Product.title.like(q), Product.description.like(q)))
        else:
            return product_filter

    @staticmethod
    def search_by_kind(product_filter, kind):
        if kind:
            return product_filter.filter(Product.kind == kind)
        else:
            return product_filter

    @staticmethod
    def search_orderby_time(product_filter, time):
        if time:
            return product_filter.order_by(Product.create_time)
        else:
            return product_filter.order_by(desc(Product.create_time))

    @staticmethod
    def search_orderby_price(product_filter, time):
        if time:
            return product_filter.order_by(Product.currentPrice)
        else:
            return product_filter.order_by(desc(Product.currentPrice))