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
    return render_template('admin/testimonial/testimonial_settings_dashboard.html')

@admin.route('/add/testimonial', methods=['Get', 'POST'])
@login_required
def add_testimonial():
    org = Organisation.query.get(1)
    form = TestimonialForm()

    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Testimonial(image=image,
                    owner_organisation=org.org_name,
                    organisation_id=org.id,
                    person_name = form.person_name.data,
                    job_title = form.job_title.data,
                    description = form.description.data              
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Testimonial added!', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial/add_testimonial.html', form=form, org=org)


@admin.route('/<int:testimonial_id>/testimonial/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(testimonial_id):
    org = Organisation.query.get(1)
    settings = Testimonial.query.filter_by(id=testimonial_id).first_or_404()
    photo = Testimonial.query.filter_by(id=testimonial_id).first_or_404()
    url = images.url(photo.image)
    form = TestimonialForm(obj=settings)
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Testimonial(image=image,
                    owner_organisation=org.org_name,
                    organisation_id=org.id,
                    person_name = form.person_name.data,
                    job_title = form.job_title.data,
                    description = form.description.data  
                          )
        db.session.add(appt)
        db.session.commit()
    #if request.method == 'POST' and 'image' in request.files:
       # image = images.save(request.files['image'])
        #form.populate_obj(settings)
        #db.session.add(settings)
        #db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.testimonial_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/testimonial/edit_testimonial.html', form=form, url=url)


@admin.route('/testimonial', defaults={'page': 1}, methods=['GET'])
@admin.route('/testimonial/<int:page>', methods=['GET'])
@login_required
@admin_required
def testimonials(page):
    testimonials = Testimonial.query.paginate(page, per_page=100)
    return render_template('admin/testimonial/browse.html', testimonials=testimonials)


@admin.route('/testimonial/<int:testimonial_id>/_delete', methods=['POST'])
@login_required
@admin_required
def delete_testimonial(testimonial_id):
    testimonial = Testimonial.query.filter_by(id=testimonial_id).first()
    db.session.delete(testimonial)
    db.session.commit()
    flash('Successfully deleted a testimonial member.', 'success')
    return redirect(url_for('admin.testimonials'))
