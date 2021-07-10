from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, and_, or_

from app.libs.time_transform import time_to_int
from app.models.address import Addressinfo
from app.models.base import Base, db
from app.models.product import Product
from app.models.user import User


class Transaction(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    price = Column(SmallInteger, nullable=False, default=100)
    state = Column(String(1), nullable=False, default='0')
    address = Column(String(100))
    star = Column(Integer, default=5)
    evaluation = Column(String(1000))

    def __init__(self):
        if self.create_time is None:
            super(Transaction, self).__init__()

    def keys(self):
        return ['id', 'user_id', 'product_id', 'price',
                'state', 'address', 'create_datetime']

    @staticmethod
    def add(form, user_id):
        with db.auto_commit():
            transaction = Transaction().query.filter_by(product_id=form.product_id.data,
                                                        user_id=user_id).first()
            if not transaction:
                transaction = Transaction()
            transaction.user_id = user_id
            transaction.product_id = form.product_id.data
            transaction.price = Product().query.with_entities(Product.originalPrice)\
                .filter_by(id=form.product_id.data).first_or_404()[0]
            transaction.address = Addressinfo().query.with_entities(Addressinfo.address)\
                .filter_by(user_id=user_id).first_or_404()[0]
            db.session.add(transaction)

    @staticmethod
    def get_user_transactions(user_id, begin, page):
        return db.session.query(User.nickname, Transaction.user_id, Transaction.create_time,
                                Transaction.state, Transaction.id, Transaction.price,
                                Transaction.address). \
            filter(or_
                   (and_(Transaction.user_id == user_id,
                         User.id == user_id),
                    (and_(User.id == user_id,
                          Product.user_id == user_id,
                          Product.id == Transaction.product_id))
                    )
                   ).limit(page).offset(begin).all()
        # Transaction.query.filter_by(user_id=user_id).limit(page).offset(begin).all()

    @staticmethod
    def verify_buyer_transaction(user_id, transaction_id):
        return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first_or_404()

    @staticmethod
    def verify_seller_transaction(user_id, transaction_id):
        return Transaction.query.join(Product) \
            .filter(Transaction.id == transaction_id) \
            .filter(Product.user_id == user_id) \
            .first_or_404()
