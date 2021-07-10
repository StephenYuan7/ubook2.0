from sqlalchemy import Column, Integer, ForeignKey, String

from app.models.base import Base, db


class Store(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(100))
    phone = Column(String(100))
    address = Column(String(100))
    description = Column(String(1000))

    def __init__(self):
        if self.create_time is None:
            super(Store, self).__init__()

    def keys(self):
        return ['id', 'user_id', 'name', 'phone', 'address', 'description', 'create_datetime']

    @staticmethod
    def create(uid, name, phone, address, description):
        store = Store.query.filter_by(user_id=uid).first()
        with db.auto_commit():
            if not store:
                store = Store()
            store.user_id = uid
            store.name = name
            store.phone = phone
            store.address = address
            store.description = description
            db.session.add(store)

    @staticmethod
    def get(uid):
        return Store.query.filter_by(user_id=uid).first_or_404()
