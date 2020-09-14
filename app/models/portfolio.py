from app import db
from datetime import datetime
from logging import log
from time import time


class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_name = db.Column(db.String)
    portfolio_title = db.Column(db.String)
    portfolio_category = db.Column(db.String)
    portfolio_price = db.Column(db.Float)
    portfolio_description = db.Column(db.Text)
    currency = db.Column(db.String)
    
    image = db.Column(db.String, default=None, nullable=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
