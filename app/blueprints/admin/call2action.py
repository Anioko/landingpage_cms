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




@admin.route('/settings/calltoaction/')
@login_required
@admin_required
def calltoaction_dashboard():
    """Frontend dashboard page."""
    return render_template('admin/frontend_settings_dashboard.html')


@admin.route('/add/call2action', methods=['Get', 'POST'])
@login_required
def add_call2action():
    org = Organisation.query.get(1)
    form = Call2actionForm()

    if request.method == 'POST':
        
        appt = Call2action(owner_organisation=org.org_name,
                     organisation_id=org.id,
                     description = form.description.data,
                     call2action_url = form.call2action_url.data,
                     action_title = form.action_title.data,
                     action_button_text = form.action_button_text.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Call2action added!', 'success')
        return redirect(url_for('admin.edit_call2action', call2action_id=org.id))
    return render_template('admin/call2action/add_call2action.html', form=form, org=org)


@admin.route('/<int:call2action_id>/call2action/edit', methods=['GET', 'POST'])
@login_required
def edit_call2action(call2action_id):
    settings = Call2action.query.filter_by(id=call2action_id).first_or_404()
    form = Call2actionForm(obj=settings)    
    if request.method == 'POST':
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.frontend_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/call2action/edit_call2action.html', form=form)
