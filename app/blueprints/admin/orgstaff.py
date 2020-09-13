from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
import commonmark
from app import db
from app.decorators import admin_required
from app.email import send_email
from flask_rq import get_queue
from app.models import *
from app.blueprints.admin.views import admin
from wtforms import Flags
from .forms import *

from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed

images = UploadSet('images', IMAGES)
photos = UploadSet('photos', IMAGES)




@admin.route('/settings/orgstaff/')
@login_required
@admin_required
def orgstaff_dashboard():
    """Portfolio dashboard page."""
    return render_template('admin/orgstaff_settings_dashboard.html')

@admin.route('/add/orgstaff', methods=['Get', 'POST'])
@login_required
def add_orgstaff():
    org = Organisation.query.get(1)
    form = OrgStaffForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            organisation_name=org.org_name,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user.id,
            added_by=current_user.full_name,
            invite_link=invite_link,
        )
        staff = OrgStaff(user_id=user.id, added_by=current_user.full_name, org_id=org.id)
        db.session.add(staff)
        db.session.commit()
        flash('User {} successfully invited'.format(user.full_name),
              'form-success')
        flash('OrgStaff added!', 'success')
        return redirect(url_for('admin.edit_orgstaff', orgstaff_id=org.id))
    return render_template('admin/orgstaff/add_orgstaff.html', form=form, org=org)


@admin.route('/<int:orgstaff_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_orgstaff(orgstaff_id):
    org = Organisation.query.filter_by(user_id=current_user.id).first_or_404()
    settings = OrgStaff.query.filter_by(id=orgstaff_id).first_or_404()
    photo = OrgStaff.query.filter_by(id=orgstaff_id).first_or_404()
    url = images.url(photo.image)
    form = OrgStaff(obj=settings)
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = OrgStaff(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                      orgstaff_name = form.orgstaff_name.data,
                      orgstaff_title = form.orgstaff_title.data,
                      orgstaff_description = form.orgstaff_description.data
                          )
        db.session.add(appt)
        db.session.commit()
    #if request.method == 'POST' and 'image' in request.files:
       # image = images.save(request.files['image'])
        #form.populate_obj(settings)
        #db.session.add(settings)
        #db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/orgstaff/edit_orgstaff.html', form=form, url=url)

