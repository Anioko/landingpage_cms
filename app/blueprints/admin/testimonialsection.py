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


@admin.route('/add/testimonialsection', methods=['Get', 'POST'])
@login_required
def add_testimonialsection():
    org = Organisation.query.get(1)
    form = TestimonialsectionForm()
    if request.method == 'POST':
        appt = Testimonialsection(owner_organisation=org.org_name,
                     organisation_id=org.id,
                    section_name = form.section_name.data,
                    section_description = form.section_description.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Testimonialsection added!', 'success')
        return redirect(url_for('admin.edit_testimonialsection', testimonialsection_id=org.id))
    return render_template('admin/testimonialsection/add_testimonialsection.html', form=form, org=org)


@admin.route('/<int:testimonialsection_id>/testimonialsection/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonialsection(testimonialsection_id):
    settings = Testimonialsection.query.filter_by(id=testimonialsection_id).first_or_404()
    form = TestimonialsectionForm(obj=settings)    
    if request.method == 'POST':
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/testimonialsection/edit_testimonialsection.html', form=form)
