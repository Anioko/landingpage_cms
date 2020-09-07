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

@admin.route('/portfolio-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def portfolio_setting(id=None):
    """Adds information to the portfolio page."""
    settings = db.session.query(Portfolio.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_portfolio_setting', id=1))
    form = PortfolioForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = None
            if request.files['photo']:
                image_filename = images.save(request.files['photo'])
            settings = Portfolio(
                portfolio_name = form.portfolio_name.data,
                portfolio_title = form.portfolio_title.data,
                portfolio_description = form.portfolio_description.data,
                image_filename=image_filename,
                organisation_id=org_id,               
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_portfolio_setting', id=id))
    return render_template('admin/new_portfolio_setting.html', form=form)

@admin.route('/edit-portfolio-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_portfolio_setting(id):
    """Edit information to the portfolio page."""
    settings = Portfolio.query.get(id)
    form = PortfolioForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.portfolio_dashboard'))
    return render_template('admin/edit_portfolio_setting.html', form=form)


@