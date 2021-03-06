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
    return render_template('admin/portfolio/portfolio_settings_dashboard.html')

@admin.route('/add/portfolio', methods=['Get', 'POST'])
@login_required
def add_portfolio():
    org = Organisation.query.get(1)
    form = PortfolioForm()

    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Portfolio(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                      portfolio_name = form.portfolio_name.data,
                      portfolio_title = form.portfolio_title.data,
                      portfolio_category = form.portfolio_category.data,
                      portfolio_price = form.portfolio_price.data,
                      currency = form.currency.data,
                      portfolio_description = form.portfolio_description.data
                          )
        db.session.add(appt)
        db.session.commit()
        flash('Portfolio added!', 'success')
        return redirect(url_for('admin.portfolios'))
    return render_template('admin/portfolio/add_portfolio.html', form=form, org=org)


@admin.route('/<int:portfolio_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio(portfolio_id):
    org = Organisation.query.get(1)
    settings = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    photo = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    url = images.url(photo.image)
    form = PortfolioForm(obj=settings)
    if request.method == 'POST' and 'image' in request.files:
        image = images.save(request.files['image'])
        appt = Portfolio(image=image,
                      owner_organisation=org.org_name,
                      organisation_id=org.id,
                      portfolio_name = form.portfolio_name.data,
                      portfolio_title = form.portfolio_title.data,
                      portfolio_category = form.portfolio_category.data,
                      portfolio_price = form.portfolio_price.data,
                      currency = form.currency.data,
                      portfolio_description = form.portfolio_description.data
                          )
        db.session.add(appt)
        db.session.commit()
    #if request.method == 'POST' and 'image' in request.files:
       # image = images.save(request.files['image'])
        #form.populate_obj(settings)
        #db.session.add(settings)
        #db.session.commit()
        flash('Data edited!', 'success')
        return redirect(url_for('admin.portfolio_dashboard'))
    else:
        flash('Error! Data was not added.', 'error')
    return render_template('admin/portfolio/edit_portfolio.html', form=form, url=url)

@admin.route('/portfolio', defaults={'page': 1}, methods=['GET'])
@admin.route('/portfolio/<int:page>', methods=['GET'])
@login_required
@admin_required
def portfolios(page):
    portfolios = Portfolio.query.paginate(page, per_page=100)
    return render_template('admin/portfolio/browse.html', portfolios=portfolios)


@admin.route('/portfolio/<int:portfolio_id>/_delete', methods=['GET'])
@login_required
@admin_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()
    db.session.delete(portfolio)
    db.session.commit()
    flash('Successfully deleted an item.', 'success')
    return redirect(url_for('admin.portfolios'))


