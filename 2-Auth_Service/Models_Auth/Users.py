from sqlalchemy import Boolean, Column, Integer, String, DateTime
from databas import Base


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255))
    password = Column(String(255), nullable=False)
    profile_pic = Column(String(255))
    address = Column(String(255))
    status = Column(Boolean, default=False)
    reset_password_token = Column(String(255))
    reset_password_token_expired = Column(DateTime)
    token = Column(String(500))


    def to_dict(self):
        user_dict =  {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'status': self.status,
            'reset_password_token': self.reset_password_token,
            'reset_password_token_expired': self.reset_password_token_expired,
            'token': self.token
        }
        return user_dict