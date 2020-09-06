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




@admin.route('/settings/brands/')
@login_required
@admin_required
def brands_dashboard():
    """Brands dashboard page."""
    return render_template('admin/brands_settings_dashboard.html')

@admin.route('/brands-brand-settings', methods=['GET', 'POST'])
@admin.route('/brands-brand-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def brands_brand_setting(id=None):
    """Adds information to the brands page."""
    settings = db.session.query(OurBrand.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_brands_brand_setting', id=1))
    form = OurBrandForm()
    if request.method == 'POST':
            settings = OurBrand(

                brand_name_one = form.brand_name_one.data,
                brand_name_two = form.brand_name_two.data,
                brand_name_three = form.brand_name_three.data,
                brand_name_five = form.brand_name_five.data,
                brand_url_one = form.brand_url_five.data,
                brand_url_two = form.brand_url_five.data,
                brand_url_three = form.brand_url_five.data,
                brand_url_four = form.brand_url_five.data,
                brand_url_five = form.brand_url_five.data,
                organisation_id=org_id,
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_brands_brand_setting', id=id))
    return render_template('admin/new_brands_brand_setting.html', form=form)


@admin.route('/edit-brands-brand-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_brands_brand_setting(id):
    """Edit information to the brands page."""
    settings = OurBrand.query.get(id)
    form = OurBrandForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.brands_dashboard'))
    return render_template('admin/new_brands_brand_setting.html', form=form)
