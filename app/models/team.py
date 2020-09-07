from app import db

from datetime import datetime
from logging import log
from time import time

class Team(db.Model):
    __tablename__ = 'teammembers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    job_title = db.Column(db.String)
    job_description = db.Column(db.String)
    team_member_facebook = db.Column(db.String)
    team_member_twitter = db.Column(db.String)
    team_member_picture = db.Column(db.String)
    team_member_linkedin = db.Column(db.String)

    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=False)
    owner_organisation = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
