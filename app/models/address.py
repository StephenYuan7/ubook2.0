from sqlalchemy import Column, Integer, ForeignKey, String

from app.models.base import Base, db


class Addressinfo(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    phone = Column(String(100))
    address = Column(String(100))

    def __init__(self):
        if self.create_time is None:
            super(Addressinfo, self).__init__()

    def keys(self):
        return ['id', 'user_id', 'phone', 'address', 'create_datetime']

    @staticmethod
    def create(uid, phone, address):
        addressinfo = Addressinfo().query.filter(Addressinfo.user_id == uid).first()
        with db.auto_commit():
            if not addressinfo:
                addressinfo = Addressinfo()
                addressinfo.status = 1
            addressinfo.user_id = uid
            addressinfo.phone = phone
            addressinfo.address = address
            db.session.add(addressinfo)

    @staticmethod
    def get(uid):
        return Addressinfo.query.filter_by(user_id=uid).first()

    @staticmethod
    def verify_user_address(user_id, address_id):
        return Addressinfo.query.filter_by(id=address_id, user_id=user_id).first_or_404()
