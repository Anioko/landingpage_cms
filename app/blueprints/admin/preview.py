from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
import commonmark
from app import db
from app.decorators import admin_required
from app.models import *
from app.blueprints.admin.views import admin
from wtforms import Flags
from .forms import *

from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed

images = UploadSet('images', IMAGES)
photos = UploadSet('photos', IMAGES)




@admin.route('/settings/preview/')
@login_required
@admin_required
def preview():
    """Preview landing page."""
    appt = Organisation.query.get(1)
    about = About.query.get(1)
    team = Team.query.all()
    portfolio = Portfolio.query.all()
    services = Service.query.all()
    testimonial = Testimonial.query.all()
    call2action = Call2action.query.get(1)
    socials = Social.query.get(1)
    teamsection = Teamsection.query.get(1)
    testimonialsection = Testimonialsection.query.get(1)
    if appt.org_industry == "Small Business":
        return render_template('public/enno/index.html',
                               appt=appt, about=about, portfolio=portfolio,
                               services=services, testimonial=testimonial,
                               call2action=call2action, socials=socials,
                               team=team, teamsection=teamsection,
                               testimonialsection=testimonialsection)
    elif appt.org_industry == "Church":
        return render_template('public/dewi/index.html',
                               appt=appt, about=about, portfolio=portfolio,
                               services=services, testimonial=testimonial,
                               call2action=call2action, socials=socials,
                               team=team, teamsection=teamsection,
                               testimonialsection=testimonialsection)
    
    elif appt.org_industry == "Restaurant":
        return render_template('public/delicious/index.html',
                               appt=appt, about=about, portfolio=portfolio,
                               services=services, testimonial=testimonial,
                               call2action=call2action, socials=socials,
                               team=team, teamsection=teamsection,
                               testimonialsection=testimonialsection)
    else:
        return render_template('public/onepage/index.html',
                               appt=appt, about=about, portfolio=portfolio,
                               services=services, testimonial=testimonial,
                               call2action=call2action, socials=socials,
                               team=team, teamsection=teamsection,
                               testimonialsection=testimonialsection)


@admin.route('/<int:portfolio_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def portfolio_details(portfolio_id):
    """Preview details page."""
    appt = Organisation.query.get(1)
    about = About.query.get(1)
    team = Team.query.all()
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    services = Service.query.all()
    testimonial = Testimonial.query.all()
    call2action = Call2action.query.get(1)
    socials = Social.query.get(1)
    teamsection = Teamsection.query.get(1)
    testimonialsection = Testimonialsection.query.get(1)
    return render_template('public/enno/portfolio-details.html',
                                   appt=appt, about=about, portfolio=portfolio,
                               services=services, testimonial=testimonial,
                               call2action=call2action, socials=socials,
                               team=team, teamsection=teamsection,
                               testimonialsection=testimonialsection)

