from app import db
from datetime import datetime
from logging import log
from time import time

class Tracking(db.Model):
    __tablename__ = 'trackings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_analytics_id = db.Column(db.String(25), unique=True)
    other_tracking_analytics_one = db.Column(db.Text)
    other_tracking_analytics_two = db.Column(db.Text)
    other_tracking_analytics_three = db.Column(db.Text)
    other_tracking_analytics_four = db.Column(db.Text)
    other_tracking_analytics_five = db.Column(db.Text)
    other_tracking_analytics_six = db.Column(db.Text)
    
    user = db.relationship("User")
    
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
