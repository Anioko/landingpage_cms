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




@admin.route('/settings/uploads/')
@login_required
@admin_required
def uploads_dashboard():
    """Uploads dashboard page."""
    return render_template('admin/uploads_settings_dashboard.html')

@admin.route('/upload', methods=['GET', 'POST'])
def image_upload():
    
    owner_organisation = db.session.query(Organisation).filter_by(user_id=current_user.id).first()
    form = PhotoForm()
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        image = Photo(image=image,
                      owner_organisation=owner_organisation.org_name,
                      organisation_id=owner_organisation.id)
        db.session.add(image)
        db.session.commit()
        flash("Photo saved.")
        return redirect(url_for('admin.show', id=image.id))
    return render_template('admin/upload/upload.html', form=form)

@admin.route('/image/<int:id>')
def show(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404)
    url = images.url(photo.image)
    return render_template('admin/upload/show.html', url=url, photo=photo)

