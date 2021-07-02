from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    profile = Column(String(100), default='default.jpg')
    real_name = Column(String(50), nullable=False)
    user_academy = Column(String(30), nullable=False)
    nickname = Column(String(30), nullable=False)
    school_id = Column(Integer)     # 后面加外键
    user_grade = Column(String(7), nullable=False)
    student_number = Column(String(10), nullable=False, unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    def __init__(self):
        if self.create_time is None:
            super(User, self).__init__()

    @staticmethod
    def register(real_name, user_academy, nickname, school_id, user_grade, student_number, password):
        with db.auto_commit():
            user = User()
            user = User.fill_information(user, nickname, real_name, school_id, student_number, user_academy, user_grade)
            user.password = password

            db.session.add(user)

    @staticmethod
    def reset(user, real_name, user_academy, nickname, school_id, user_grade, student_number):
        User.fill_information(user, nickname, real_name, school_id, student_number, user_academy, user_grade)

    @staticmethod
    def fill_information(user, nickname, real_name, school_id, student_number, user_academy, user_grade):
        """
        填充除了密码的信息
        :param user:
        :param nickname:
        :param real_name:
        :param school_id:
        :param student_number:
        :param user_academy:
        :param user_grade:
        """
        user.real_name = real_name
        user.user_academy = user_academy
        user.nickname = nickname
        user.school_id = school_id
        user.user_grade = user_grade
        user.student_number = student_number
        return user

    def keys(self):
        return ['id', 'profile', 'real_name', 'user_academy',
                'nickname', 'school_id', 'user_grade',
                'student_number']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def verify(student_number, password):
        user = User.query.filter_by(student_number=student_number).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
