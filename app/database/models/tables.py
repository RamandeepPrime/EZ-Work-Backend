
from sqlalchemy import Boolean, Column, String, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT

from resources.userTypes import UserTypes

from ..db import Base

class User(Base):

    __tablename__ = 'Users'

    id = Column(INTEGER(11), primary_key=True, autoincrement = True)
    email = Column(String(200), nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)
    emailVerfied = Column(Boolean, default=False)
    isDisabled = Column(Boolean, default=False)
    # userType = Column(ENUM(UserTypes), default='Client')
    userType= Column(String(11), default='Client')