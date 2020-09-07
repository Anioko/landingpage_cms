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




@admin.route('/settings/team/')
@login_required
@admin_required
def team_dashboard():
    """Team dashboard page."""
    return render_template('admin/team_settings_dashboard.html')

@admin.route('/landing-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def team_setting(id=None):
    """Adds information to the team page."""
    #org_id = db.session.query(Organisation.id).count()
    settings = db.session.query(Team.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_team_setting', id=1))
    form = TeamForm()
    if request.method == 'POST':
            settings = Team(
                name = form.name.data,
                job_title = form.job_title.data,
                job_description = form.job_description.data,
                #organisation_id=org_id,                
                team_member_twitter = form.team_member_twitter.data,
                team_member_facebook = form.team_member_facebook.data,
                team_member_linkedin = form.team_member_linkedin.data,
                team_member_picture = form.team_member_picture.data

            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_team_setting', id=id))
    return render_template('admin/team/new_team_setting.html', form=form)

@admin.route('/edit-team-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_team_setting(id):
    """Edit information to the team page."""
    settings = Team.query.get(id)
    form = TeamForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_team_setting.html', form=form)

