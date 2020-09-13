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


@admin.route('/add/team', methods=['Get', 'POST'])
@login_required
def add_team():
    org = Organisation.query.get(1)
    form = TeamForm()

    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Team(image=image,
                    owner_organisation=org.org_name,
                    organisation_id=org.id,
                    name = form.name.data,
                    job_title = form.job_title.data,
                    job_description = form.job_description.data,              
                    team_member_twitter = form.team_member_twitter.data,
                    team_member_facebook = form.team_member_facebook.data,
                    team_member_linkedin = form.team_member_linkedin.data,
                    team_member_instagram = form.team_member_instagram.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Team added!', 'success')
        return redirect(url_for('admin.edit_team', team_id=org.id))
    return render_template('admin/team/add_team.html', form=form, org=org)


@admin.route('/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    org = Organisation.query.get(1)
    settings = Team.query.filter_by(id=team_id).first_or_404()
    photo = Team.query.filter_by(id=team_id).first_or_404()
    url = images.url(photo.image)
    form = TeamForm(obj=settings)
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Team(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                    name = form.name.data,
                    job_title = form.job_title.data,
                    job_description = form.job_description.data,              
                    team_member_twitter = form.team_member_twitter.data,
                    team_member_facebook = form.team_member_facebook.data,
                    team_member_linkedin = form.team_member_linkedin.data,
                    team_member_instagram = form.team_member_instagram.data
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
    return render_template('admin/team/edit_team.html', form=form, url=url)
