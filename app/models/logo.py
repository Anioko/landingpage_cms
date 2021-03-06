from app import db

from datetime import datetime
from logging import log
from time import time

class Logo(db.Model):
    __tablename__ = 'logos'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, default=None, nullable=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
