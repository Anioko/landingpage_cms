from app import db
from datetime import datetime
from logging import log
from time import time

class Social(db.Model):
    __tablename__ = 'socials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    twitter_name = db.Column(db.String(25), unique=True)
    facebook_name = db.Column(db.String(25), unique=True)
    instagram_name = db.Column(db.String(25), unique=True)
    linkedin_name = db.Column(db.String(25), unique=True)
    tiktok_name = db.Column(db.String(25), unique=True)
    snap_chat_name = db.Column(db.String(25), unique=True)
    youtube = db.Column(db.String(25), unique=True)
    user = db.relationship("User")
    
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
