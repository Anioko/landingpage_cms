from app import db
from datetime import datetime
from logging import log
from time import time


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    brand_name_one = db.Column(db.String(25), unique=True)
    brand_name_two = db.Column(db.String(25), unique=True)
    brand_name_three = db.Column(db.String(25), unique=True)
    brand_name_four = db.Column(db.String(25), unique=True)
    brand_name_five = db.Column(db.String(25), unique=True)
    brand_url_one = db.Column(db.String(25), unique=True)
    brand_url_two = db.Column(db.String(25), unique=True)
    brand_url_three = db.Column(db.String(25), unique=True)
    brand_url_four = db.Column(db.String(25), unique=True)
    brand_url_five = db.Column(db.String(25), unique=True)

    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
