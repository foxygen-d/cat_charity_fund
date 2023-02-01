from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey

from .abstract import Abstract


class Donation(Abstract):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
