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

@admin.route('/calltoaction-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def calltoaction_setting(id=None):
    """Adds information to the calltoaction."""
    settings = db.session.query(Calltoaction.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_calltoaction_setting', id=1))
    form = CalltoactionForm()
    if request.method == 'POST':
            settings = Calltoaction(
                description = form.description.data,
                organisation_id=org_id,
                call2action_url = form.call2action_url.data,
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_call2action_setting', id=id))
    return render_template('admin/new_call2action_setting.html', form=form)

@admin.route('/edit-call2action-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_call2action_setting(id):
    """Edit information to the landing page."""
    settings = Call2action.query.get(id)
    form = Call2actionForm(obj=settings)    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.frontend_dashboard'))
    return render_template('admin/edit_call2action_setting.html', form=form)
