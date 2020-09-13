from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, send_from_directory
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
import imghdr
from werkzeug.utils import secure_filename

images = UploadSet('images', IMAGES)


@admin.route('/settings/uploads/')
@login_required
@admin_required
def uploads_dashboard():
    """Uploads dashboard page."""
    return render_template('admin/upload/uploads_settings_dashboard.html')

@admin.route('/upload')
def upload_file():
   return render_template('admin/upload/upload_dropzone.html')
	
@admin.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['image']
      f.save(request.files['image'])
      f = Photo(image=request.files['image'],
                      owner_organisation=Organisation.org_name,
                      organisation_id=Organisation.id)
      db.session.add(f)
      db.session.commit()
      flash("Photo saved.")
      return 'file uploaded successfully'
    
@admin.route('/uploads', methods=['GET', 'POST'])
def image_upload():
    
    org = Organisation.query.get(1)
    #form = PhotoForm()
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        image = Photo(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id)
        image.store()
        db.session.add(image)
        db.session.commit()
        flash("Photo saved.")
        return redirect(url_for('admin.show', id=image.id))
    return render_template('admin/upload/upload_dropzone.html')

@admin.route('/image/<int:id>')
def show(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404)
    url = images.url(photo.image)
    return render_template('admin/upload/show.html', url=url, photo=photo)


@admin.route('/image', defaults={'page': 1}, methods=['GET'])
@admin.route('/image/<int:page>', methods=['GET'])
@login_required
@admin_required
def images(page):
    images = Photo.query.paginate(page, per_page=100)
    return render_template('admin/upload/browse.html', images=images)


@admin.route('/image/<int:img_id>/delete', methods=['GET'])
@login_required
@admin_required
def delete_img(img_id):
    img = Photo.query.filter_by(id=img_id).one()
    db.session.delete(img)
    db.session.commit()
    flash('Successfully deleted Image.', 'success')
    return redirect(url_for('admin.uploads_dashboard'))
