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




@admin.route('/settings/about/')
@login_required
@admin_required
def about_dashboard():
    """About dashboard page."""
    return render_template('admin/about_settings_dashboard.html')



@admin.route('/add/about', methods=['Get', 'POST'])
@login_required
def add_about():
    org = Organisation.query.get(1)
    form = AboutForm()

    if request.method == 'POST':
        
        appt = About(owner_organisation=org.org_name,
                     organisation_id=org.id,
                     description = form.description.data,
                     about_us_title = form.about_us_title.data,
                     key_information_title_one = form.key_information_title_one.data,
                     key_information_title_two = form.key_information_title_two.data,
                     key_information_title_three = form.key_information_title_three.data,
                 
                     key_information_description_one = form.key_information_description_one.data,
                     key_information_description_two = form.key_information_description_two.data,
                     key_information_description_three = form.key_information_description_three.data,
                 
                     key_information_icon_one = form.key_information_icon_one.data,
                     key_information_icon_two = form.key_information_icon_two.data,
                     key_information_icon_three = form.key_information_icon_three.data,

                     key_information_numbers_one = form.key_information_numbers_one.data,
                     key_information_numbers_two = form.key_information_numbers_two.data,
                     key_information_numbers_three = form.key_information_numbers_three.data,
                     key_information_numbers_four = form.key_information_numbers_four.data,
                 
                     key_information_numbers_description_one = form.key_information_numbers_description_one.data,
                     key_information_numbers_description_two = form.key_information_numbers_description_two.data,
                     key_information_numbers_description_three = form.key_information_numbers_description_three.data,
                     key_information_numbers_description_four = form.key_information_numbers_description_four.data 
                          )
        db.session.add(appt)
        db.session.commit()
        flash('About added!', 'success')
        return redirect(url_for('admin.edit_about', about_id=org.id))
    return render_template('admin/about/add_about.html', form=form, org=org)


@admin.route('/<int:about_id>/about/edit', methods=['GET', 'POST'])
@login_required
def edit_about(about_id):
    settings = About.query.filter_by(id=about_id).first_or_404()
    form = AboutForm(obj=settings)    
    if request.method == 'POST':
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/about/edit_about.html', form=form)


