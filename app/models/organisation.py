from app import db
from datetime import datetime
from logging import log
from time import time

class Organisation(db.Model):
    __tablename__ = 'organisations'
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    #image_filename = db.Column(db.String, default=None, nullable=True)
    #image_url = db.Column(db.String, default=None, nullable=True)
    org_name = db.Column(db.String(255))
    org_city = db.Column(db.String(255))
    org_state = db.Column(db.String(255))
    org_country = db.Column(db.String(255))
    org_website = db.Column(db.String(255))
    org_short_description = db.Column(db.String(255))
    org_industry = db.Column(db.String(255))
    org_description = db.Column(db.Text)
    logos = db.relationship('Logo', backref='organisation', lazy='dynamic')
    teams = db.relationship('Team', backref='organisation', lazy='dynamic')
    services = db.relationship('Service', backref='organisation', lazy='dynamic')
    testimonials = db.relationship('Testimonial', backref='organisation', lazy='dynamic')   
    portfolios = db.relationship('Portfolio', backref='organisation', lazy='dynamic')
    users = db.relationship('User', backref='organisation', lazy='dynamic')
    
    #users = db.relationship('User', backref='organisation', foreign_keys='Organisation.user_id')
   
    #user = db.relationship('User', backref='organisations', cascade='all, delete')
    #users = db.relationship('User', backref='organisation', lazy='dynamic',
                        #primaryjoin="Organisation.id == User.organisation_id")
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)

    def get_staff(self):
        ids = [user.user_id for user in self.staff]
        return User.query.filter(User.id.in_(ids)).all()

    def get_photo(self):
        if self.image_filename:
            return url_for('_uploads.uploaded_file', setname='images', filename=self.image_filename, _external=True)
        else:
            return url_for('static', filename="images/medium_logo_default.png")
