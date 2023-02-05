from sqlalchemy import Column, String, Text

from .abstract import Abstract


class CharityProject(Abstract):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
