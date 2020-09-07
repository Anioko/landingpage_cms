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




@admin.route('/settings/newslink/')
@login_required
@admin_required
def newslink_dashboard():
    """Newslink dashboard page."""
    return render_template('admin/newslink_settings_dashboard.html')


@admin.route('/newslink-settings', methods=['GET', 'POST'])
@admin.route('/newslink-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def newslink_setting(id=None):
    """Adds information to the landing page."""
    settings = db.session.query(NewsLink.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_newslink_setting', id=1))
    form = NewsLinkForm()
    if request.method == 'POST':
            settings = NewsLink(

                news_site_one = form.news_site_one.data,
                news_site_two = form.news_site_two.data,
                news_site_three = form.news_site_three.data,
                news_site_five = form.news_site_five.data,
                news_url_one = form.news_url_five.data,
                news_url_two = form.news_url_five.data,
                news_url_three = form.news_url_five.data,
                news_url_four = form.news_url_five.data,
                news_url_five = form.news_url_five.data
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_newslink_setting', id=id))
    return render_template('admin/newslink_edit_setting.html', form=form)


@admin.route('/edit-newslink-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_newslink_setting(id):
    """Edit information to the landing page."""
    settings = NewsLink.query.get(id)
    form = NewsLinkForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.newslink_dashboard'))
    return render_template('admin/newslink_edit_setting.html', form=form)
