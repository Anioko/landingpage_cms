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



@admin.route('/add/social', methods=['Get', 'POST'])
@login_required
def add_social():
    org = Organisation.query.get(1)
    form = SocialForm()
    if request.method == 'POST':
        appt = Social(owner_organisation=org.org_name,
                      organisation_id=org.id,
                      twitter_name = form.twitter_name.data,
                      facebook_name = form.facebook_name.data,
                      instagram_name=form.instagram_name.data,
                      linkedin_name = form.linkedin_name.data,
                      tiktok_name = form.tiktok_name.data,
                      snap_chat_name = form.snap_chat_name.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Social added!', 'success')
        return redirect(url_for('admin.edit_social', social_id=org.id))
    return render_template('admin/social/add_social.html', form=form, org=org)


@admin.route('/<int:social_id>/social/edit', methods=['GET', 'POST'])
@login_required
def edit_social(social_id):
    settings = Social.query.filter_by(id=social_id).first_or_404()
    form = SocialForm(obj=settings)    
    if request.method == 'POST':
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/social/edit_social.html', form=form)

