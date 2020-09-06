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




@admin.route('/settings/portfolio/')
@login_required
@admin_required
def portfolio_dashboard():
    """Portfolio dashboard page."""
    return render_template('admin/portfolio_settings_dashboard.html')

@admin.route('/portfolio-settings', methods=['GET', 'POST'])
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def portfolio_setting(id=None):
    """Adds information to the portfolio page."""
    settings = db.session.query(Portfolio.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_portfolio_setting', id=1))
    form = PortfolioForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = None
            if request.files['photo']:
                image_filename = images.save(request.files['photo'])
            settings = Portfolio(
                portfolio_name = form.portfolio_name.data,
                portfolio_title = form.portfolio_title.data,
                portfolio_description = form.portfolio_description.data,
                image_filename=image_filename,
                organisation_id=org_id,               
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_portfolio_setting', id=id))
    return render_template('admin/new_portfolio_setting.html', form=form)

@admin.route('/edit-portfolio-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_portfolio_setting(id):
    """Edit information to the portfolio page."""
    settings = Portfolio.query.get(id)
    form = PortfolioForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.portfolio_dashboard'))
    return render_template('admin/edit_portfolio_setting.html', form=form)


@admin.route('/upload', methods=['GET', 'POST'])
def upload():
    form = LandingImageForm()
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        image = LandingImage(image=image)
        db.session.add(image)
        db.session.commit()
        flash("Photo saved.")
        return redirect(url_for('admin.show', id=image.id))
    return render_template('admin/upload.html', form=form)

@admin.route('/image/<int:id>')
def show(id):
    photo = LandingImage.query.get(id)
    if photo is None:
        abort(404)
    url = images.url(photo.image)
    return render_template('admin/show.html', url=url, photo=photo)


@admin.route('/portfolio-brand-settings', methods=['GET', 'POST'])
@admin.route('/portfolio-brand-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def portfolio_brand_setting(id=None):
    """Adds information to the portfolio page."""
    settings = db.session.query(OurBrand.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_portfolio_brand_setting', id=1))
    form = OurBrandForm()
    if request.method == 'POST':
            settings = OurBrand(

                brand_name_one = form.brand_name_one.data,
                brand_name_two = form.brand_name_two.data,
                brand_name_three = form.brand_name_three.data,
                brand_name_five = form.brand_name_five.data,
                brand_url_one = form.brand_url_five.data,
                brand_url_two = form.brand_url_five.data,
                brand_url_three = form.brand_url_five.data,
                brand_url_four = form.brand_url_five.data,
                brand_url_five = form.brand_url_five.data
            )
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully added', 'success')
            return redirect(url_for('admin.edit_portfolio_brand_setting', id=id))
    return render_template('admin/new_portfolio_brand_setting.html', form=form)


@admin.route('/edit-portfolio-brand-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_portfolio_brand_setting(id):
    """Edit information to the portfolio page."""
    settings = OurBrand.query.get(id)
    form = OurBrandForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.portfolio_dashboard'))
    return render_template('admin/new_portfolio_brand_setting.html', form=form)

@admin.route('/portfolio-news-settings', methods=['GET', 'POST'])
@admin.route('/portfolio-news-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def portfolio_news_setting(id=None):
    """Adds information to the portfolio page."""
    settings = db.session.query(NewsLink.id).count()
    if settings == 1:
        return redirect(url_for('admin.edit_portfolio_brand_setting', id=1))
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
            return redirect(url_for('admin.edit_portfolio_brand_setting', id=id))
    return render_template('admin/new_portfolio_edit_setting.html', form=form)


@admin.route('/edit-portfolio-brand-settings/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_portfolio_news_setting(id):
    """Edit information to the portfolio page."""
    settings = NewsLink.query.get(id)
    form = NewsLinkForm(obj=settings)
    
    if request.method == 'POST':
            form.populate_obj(settings)
            db.session.add(settings)
            db.session.commit()
            flash('Settings successfully edited', 'success')
            return redirect(url_for('admin.portfolio_dashboard'))
    return render_template('admin/new_portfolio_edit_setting.html', form=form)
