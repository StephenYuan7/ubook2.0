from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey

from app.libs.time_transform import time_to_int
from app.models.base import Base, db
from app.models.product import Product


class Transaction(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    price = Column(SmallInteger, nullable=False, default=100)
    state = Column(String(1), nullable=False, default='0')
    address = Column(String(100))
    order_time = Column(Integer)
    over_time = Column(Integer)
    star = Column(Integer, default=5)
    evaluation = Column(String(1000))

    def __init__(self):
        if self.create_time is None:
            super(Transaction, self).__init__()

    def keys(self):
        return ['id', 'user_id', 'product_id', 'price',
                'state', 'address', 'order_time', 'over_time',
                'create_datetime']

    @staticmethod
    def add(form, user_id):
        with db.auto_commit():
            transaction = Transaction()
            transaction.user_id = user_id
            transaction.product_id = form.product_id.data
            transaction.price = form.price.data
            transaction.address = form.address.data
            transaction.order_time = time_to_int(form.order_time.data)

            db.session.add(transaction)

    @staticmethod
    def get_user_transactions(user_id, begin, page):
        return Transaction.query.filter_by(user_id=user_id).limit(page).offset(begin).all()

    @staticmethod
    def verify_buyer_transaction(user_id, transaction_id):
        return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first_or_404()

    @staticmethod
    def verify_seller_transaction(user_id, transaction_id):
        return Transaction.query.join(Product) \
            .filter(Transaction.id == transaction_id) \
            .filter(Product.user_id == user_id) \
            .first_or_404()
