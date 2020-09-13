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
    return render_template('admin/services/service_settings_dashboard.html')



@admin.route('/add/service', methods=['Get', 'POST'])
@login_required
def add_service():
    org = Organisation.query.get(1)
    form = ServiceForm()
    if request.method == 'POST':
        appt = Service(owner_organisation=org.org_name,
                    organisation_id=org.id,
                    service_name = form.service_name.data,
                    service_icon = form.service_icon.data,
                    service_description = form.service_description.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Service added!', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/services/add_service.html', form=form, org=org)


@admin.route('/<int:service_id>/service/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    settings = Service.query.filter_by(id=service_id).first_or_404()
    form = ServiceForm(obj=settings)
    if request.method == 'POST':
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.services_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/services/edit_service.html', form=form)


@admin.route('/services', defaults={'page': 1}, methods=['GET'])
@admin.route('/services/<int:page>', methods=['GET'])
@login_required
@admin_required
def services(page):
    services = Service.query.paginate(page, per_page=100)
    return render_template('admin/services/browse.html', services=services)


@admin.route('/service/<int:service_id>/_delete', methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    service = Service.query.filter_by(id=service_id).first()
    db.session.delete(service)
    db.session.commit()
    flash('Successfully deleted a service member.', 'success')
    return redirect(url_for('admin.services'))

