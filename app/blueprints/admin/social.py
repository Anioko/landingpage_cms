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




@admin.route('/settings/social/')
@login_required
@admin_required
def social_dashboard():
    """Social dashboard page."""
    return render_template('admin/social_settings_dashboard.html')

@admin.route('/social-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def social_setting(id=None):
    """Adds information to the social."""
    settings = db.session.query(About.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_social_setting', id=1))
    form = AboutForm()
    if request.method == 'POST':
            settings = About(
                twitter_name = form.twitter_name.data,
                facebook_name = form.facebook_name.data,
                instagram_name=form.instagram_name.data,
                linkedin_name = form.linkedin_name.data,
                tiktok_name = form.tiktok_name.data,
                snap_chat_name = form.snap_chat_name.data,
                youtube = form.youtube.data,
                organisation_id=org_id,
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_social_setting', id=id))
    return render_template('admin/new_social_setting.html', form=form)

@admin.route('/edit-social-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_social_setting(id):
    """Edit information to the landing page."""
    settings = About.query.get(id)
    form = AboutForm(obj=settings)    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_social_setting.html', form=form)
