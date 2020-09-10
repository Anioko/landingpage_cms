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
def organization_dashboard():
    """Organization dashboard page."""
    return render_template('admin/organization_settings_dashboard.html')

@admin.route('/add/organization/', methods=['GET', 'POST'])
@login_required
def create_org():
    organization_exist = Organisation.query.get(1)
    if organization_exist is not None:
        return redirect(url_for('admin.edit_org', org_id=organization_exist.id))
        
    form = OrganisationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #image_filename = images.save(request.files['logo'])
            #image_url = images.url(image_filename)
            org = Organisation(
                user_id=current_user.id,
                #image_filename=image_filename,
                #image_url=image_url,
                org_name=form.org_name.data,
                org_industry=form.org_industry.data,
                org_short_description=form.org_short_description.data,
                org_website=form.org_website.data,
                org_city=form.org_city.data,
                org_state=form.org_state.data,
                org_country=form.org_country.data,
                org_description=form.org_description.data
            )
            db.session.add(org)
            db.session.commit()
            flash('Data added!', 'success')
            logo = Organisation.query.filter(Organisation.logos).first()
            if logo is None:
                return redirect(url_for('admin.logo_upload'))
            return redirect(url_for('admin.frontend_dashboard'))
        else:
            flash('Error! Data was not added.', 'error')
    return render_template('admin/organisations/create_org.html', form=form)

@admin.route('/organization/<int:org_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_org(org_id):
    """Edit information to the organisation."""
    settings = Organisation.query.filter(Organisation.user == current_user).filter_by(id=org_id).first_or_404()
    form = OrganisationForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/organisations/edit_org.html', form=form)


@admin.route('/organization', defaults={'page': 1}, methods=['GET'])
@admin.route('/organization/<int:page>', methods=['GET'])
@login_required
@admin_required
def orgs(page):
    orgs = Organisation.query.paginate(page, per_page=100)
    return render_template('admin/organisations/browse.html', orgs=orgs)


@admin.route('/organization/<int:org_id>/_delete', methods=['POST'])
@login_required
@admin_required
def delete_org(org_id):
    org = Organisation.query.filter_by(id=org_id).first()
    db.session.delete(org)
    db.session.commit()
    flash('Successfully deleted Organisation.', 'success')
    return redirect(url_for('admin.orgs'))
