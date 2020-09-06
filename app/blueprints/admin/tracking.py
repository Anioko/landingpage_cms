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




@admin.route('/settings/tracking/')
@login_required
@admin_required
def tracking_dashboard():
    """Tracking dashboard page."""
    return render_template('admin/tracking_settings_dashboard.html')

@admin.route('/tracking-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def tracking_setting(id=None):
    """Adds information to the tracking page."""
    settings = db.session.query(Tracking.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_tracking_setting', id=1))
    form = TrackingForm()
    if request.method == 'POST':
            settings = Tracking(
                organisation_id=org_id,        
                google_analytics_id = form.google_analytics_id.data,
                other_tracking_analytics_one = form.other_tracking_analytics_one.data,
                other_tracking_analytics_two = form.other_tracking_analytics_two.data,
                other_tracking_analytics_three = form.other_tracking_analytics_three.data,
                other_tracking_analytics_four = form.other_tracking_analytics_four.data,
                other_tracking_analytics_five = form.other_tracking_analytics_five.data,
                other_tracking_analytics_six = form.other_tracking_analytics_six.data,
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_tracking_setting', id=id))
    return render_template('admin/new_tracking_setting.html', form=form)

@admin.route('/edit-tracking-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tracking_setting(id):
    """Edit information to the tracking page."""
    settings = Tracking.query.get(id)
    form = TrackingForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_tracking_setting.html', form=form)

