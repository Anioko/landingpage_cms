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




@admin.route('/settings/services/')
@login_required
@admin_required
def services_dashboard():
    """Services dashboard page."""
    return render_template('admin/services_settings_dashboard.html')

@admin.route('/services-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def services_setting(id=None):
    """Adds information to the services page."""
    settings = db.session.query(Services.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_services_setting', id=1))
    form = ServicesForm()
    if request.method == 'POST':
            settings = Services(
                service_name = form.service_name.data,
                service_intro = form.service_intro.data,
                service_description = form.service_description.data,
                organisation_id=org_id   
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_services_setting', id=id))
    return render_template('admin/new_services_setting.html', form=form)

