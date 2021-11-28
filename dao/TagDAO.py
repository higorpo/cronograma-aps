import uuid

from dao.AbstractDAO import DAO
from model.Tag import Tag


class TagDAO(DAO):
    def __init__(self):
        super().__init__('dao/store/tag.pkl')

    def add(self, tag: Tag):
        if ((tag is not None) and isinstance(tag, Tag) and isinstance(tag.id, uuid.UUID)):
            super().add(tag.id, tag)

    def remove(self, tag: Tag):
        if ((tag is not None) and isinstance(tag, Tag) and isinstance(tag.id, uuid.UUID)):
            super().remove(tag.id)
