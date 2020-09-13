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




@admin.route('/settings/preview/')
@login_required
@admin_required
def preview():
    """Preview landing page."""
    appt = Organisation.query.get(1)
    if appt.org_industry == "Small Business":
        return render_template('public/enno/index.html')
    elif appt.org_industry == "Church":
        return render_template('public/dewi/index.html')
    elif appt.org_industry == "Restaurant":
        return render_template('public/delicious/index.html')
    else:
        return render_template('public/onepage/index.html')

