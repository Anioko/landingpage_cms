from app import db
from datetime import datetime
from logging import log
from time import time


class NewsLink(db.Model):
    __tablename__ = 'newslinks'

    id = db.Column(db.Integer, primary_key=True)
    news_site_one = db.Column(db.String(25), unique=True)
    news_site_two = db.Column(db.String(25), unique=True)
    news_site_three = db.Column(db.String(25), unique=True)
    news_site_four = db.Column(db.String(25), unique=True)
    news_site_five = db.Column(db.String(25), unique=True)
    news_url_one = db.Column(db.String(25), unique=True)
    news_url_two = db.Column(db.String(25), unique=True)
    news_url_three = db.Column(db.String(25), unique=True)
    news_url_four = db.Column(db.String(25), unique=True)
    brand_url_five = db.Column(db.String(25), unique=True)

    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
