from app import db
from datetime import datetime
from logging import log
from time import time

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    read = db.Column(db.Boolean, default=False)
    spam = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    name = db.Column(db.String(), default=None, nullable=True)
    email = db.Column(db.String(64), default=None, nullable=True)
    text = db.Column(db.Text)
    user = db.relationship("User")
    
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
