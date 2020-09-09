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




@admin.route('/settings/organization/')
@login_required
@admin_required
def photo_dashboard():
    """Photo dashboard page."""
    return render_template('admin/photo_settings_dashboard.html')

@organisations.route('/logo/upload', methods=['GET', 'POST'])
@login_required
def logo_upload():
    ''' check if logo already exist, if it does, send to homepage. Avoid duplicate upload here'''
    check_logo_exist = db.session.query(Logo).filter(Logo.organisation_id == Organisation.id).count()
    if check_logo_exist >= 1:
        return redirect(url_for('main.index'))
    form = LogoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = images.save(request.files['logo'])
            image_url = images.url(image_filename)
            owner_organisation = db.session.query(Organisation).filter_by(user_id=current_user.id).first()
            logo = Logo(
                image_filename=image_filename,
                image_url=image_url,
                owner_organisation=owner_organisation.org_name,
                organisation_id=owner_organisation.id
            )
            db.session.add(logo)
            db.session.commit()
            flash("Image saved.")
            return redirect(url_for('organisations.org_home'))
        else:
            flash('ERROR! Photo was not saved.', 'error')
    return render_template('organisations/upload.html', form=form)
