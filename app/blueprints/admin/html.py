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




@admin.route('/settings/html/')
@login_required
@admin_required
def html_dashboard():
    """Frontend dashboard page."""
    return render_template('admin/html_settings_dashboard.html')

@admin.route('/html-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def html_setting(id=None):
    """Adds information to the html page."""
    settings = db.session.query(Html.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_html_setting', id=1))
    form = HtmlForm()
    if request.method == 'POST':
            settings = Html(
                block_content_one = form.block_content_one.data,
                html_code_one = form.html_code_one.data,
                html_code_two = form.html_code_two.data,
                html_code_three = form.html_code_three.data,
                html_code_four = form.html_code_four.data,
                organisation_id=org_id
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_html_setting', id=id))
    return render_template('admin/new_html_setting.html', form=form)

@admin.route('/edit-html-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_html_setting(id):
    """Edit information to the html page."""
    settings = Html.query.get(id)
    form = HtmlForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.html_dashboard'))
    return render_template('admin/edit_html_setting.html', form=form)

