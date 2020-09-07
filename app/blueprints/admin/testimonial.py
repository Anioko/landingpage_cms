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




@admin.route('/settings/testimonial/')
@login_required
@admin_required
def testimonial_dashboard():
    """Testimonial dashboard page."""
    return render_template('admin/testimonial_settings_dashboard.html')

@admin.route('/testimonial-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def testimonial_setting(id=None):
    """Adds information to the testimonial page."""
    settings = db.session.query(Testimonial.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_testimonial_setting', id=1))
    form = TestimonialForm()
    if request.method == 'POST':
            settings = Testimonial(
                person_name = form.site_name.data,
                testimonial_title = form.title.data,
                description = form.description.data,
                organisation_id=org_id
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_testimonial_setting', id=id))
    return render_template('admin/new_testimonial_setting.html', form=form)

@admin.route('/edit-testimonial-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_testimonial_setting(id):
    """Edit information to the testimonial page."""
    settings = Testimonial.query.get(id)
    form = TestimonialForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.testimonial_dashboard'))
    return render_template('admin/edit_testimonial_setting.html', form=form)

