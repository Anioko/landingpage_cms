from app import db
from datetime import datetime
from logging import log
from time import time

class Html(db.Model):
    __tablename__ = 'htmls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    block_content_one = db.Column(db.Text)
    html_code_one = db.Column(db.Text)
    html_code_two = db.Column(db.Text)
    html_code_three = db.Column(db.Text)
    html_code_four = db.Column(db.Text)
    user = db.relationship("User")
    
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
