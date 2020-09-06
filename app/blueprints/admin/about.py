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

@admin.route('/about-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def about_setting(id=None):
    """Adds information to the about."""
    settings = db.session.query(About.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_about_setting', id=1))
    form = AboutForm()
    if request.method == 'POST':
            settings = About(
                description = form.description.data,
                organisation_id=org_id,
                about_us_title = db.Column.data,
                key_information_title_one = form.key_information_title_one.data,
                key_information_title_two = key_information_title_two.data,
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
                key_information_numbers_description_four = form.key_information_numbers_description_four.data, 
    
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_about_setting', id=id))
    return render_template('admin/new_about_setting.html', form=form)

@admin.route('/edit-about-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_about_setting(id):
    """Edit information to the landing page."""
    settings = About.query.get(id)
    form = AboutForm(obj=settings)    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_about_setting.html', form=form)
