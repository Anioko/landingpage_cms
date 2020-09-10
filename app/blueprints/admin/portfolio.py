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




@admin.route('/settings/portfolio/')
@login_required
@admin_required
def portfolio_dashboard():
    """Portfolio dashboard page."""
    return render_template('admin/portfolio_settings_dashboard.html')

@admin.route('/add/portfolio', methods=['Get', 'POST'])
@login_required
def add_portfolio():
    org = Organisation.query.filter_by(user_id=current_user.id).first_or_404()
    form = PortfolioForm()

    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Portfolio(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                      portfolio_name = form.portfolio_name.data,
                      portfolio_title = form.portfolio_title.data,
                      portfolio_description = form.portfolio_description.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Portfolio added!', 'success')
        return redirect(url_for('admin.edit_portfolio', portfolio_id=org.id))
    return render_template('admin/portfolio/add_portfolio.html', form=form, org=org)


@admin.route('/<int:portfolio_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio(portfolio_id):
    org = Organisation.query.filter_by(user_id=current_user.id).first_or_404()
    settings = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    photo = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    url = images.url(photo.image)
    form = PortfolioForm(obj=settings)
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Portfolio(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                      portfolio_name = form.portfolio_name.data,
                      portfolio_title = form.portfolio_title.data,
                      portfolio_description = form.portfolio_description.data
                          )
        db.session.add(appt)
        db.session.commit()
    #if request.method == 'POST' and 'image' in request.files:
       # image = images.save(request.files['image'])
        #form.populate_obj(settings)
        #db.session.add(settings)
        #db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/portfolio/edit_portfolio.html', form=form, url=url)

