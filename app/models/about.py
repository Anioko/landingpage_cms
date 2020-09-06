from app import db
from datetime import datetime
from logging import log
from time import time


class About(db.Model):
    __tablename__ = 'abouts'
    id = db.Column(db.Integer, primary_key=True)

    about_us_title = db.Column(db.String)
    key_information_title_one = db.Column(db.String)
    key_information_title_two = db.Column(db.String)
    key_information_title_three = db.Column(db.String)
 
    key_information_description_one = db.Column(db.String)
    key_information_description_two = db.Column(db.String)
    key_information_description_three = db.Column(db.String)
 
    key_information_icon_one = db.Column(db.String)
    key_information_icon_two = db.Column(db.String)
    key_information_icon_three = db.Column(db.String)

    key_information_numbers_one = db.Column(db.String)
    key_information_numbers_two = db.Column(db.String)
    key_information_numbers_three = db.Column(db.String)
    key_information_numbers_four = db.Column(db.String)
 
    key_information_numbers_description_one = db.Column(db.String)
    key_information_numbers_description_two = db.Column(db.String)
    key_information_numbers_description_three = db.Column(db.String)
    key_information_numbers_description_four = db.Column(db.String) 
    
    description = db.Column(db.Text)

    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
