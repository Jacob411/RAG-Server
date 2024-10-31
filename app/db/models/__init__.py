from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .document_group import DocumentGroup
from .document_group_item import DocumentGroupItem