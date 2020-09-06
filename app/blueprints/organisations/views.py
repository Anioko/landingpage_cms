from flask import Blueprint, render_template, abort, flash, redirect, request
from flask_login import current_user, login_required

from app.decorators import admin_required
from app.email import send_email
from .forms import *

organisations = Blueprint('organisations', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@organisations.route('/home')
@login_required
def org_home():
    orgs = current_user.organisations + Organisation.query.join(OrgStaff, Organisation.id == OrgStaff.org_id). \
        filter(OrgStaff.user_id == current_user.id).all()
    return render_template('organisations/org_dashboard.html', orgs=orgs)


@organisations.route('/org/<org_id>')
@login_required
def select_org(org_id):
    org = Organisation.query.filter_by(id=org_id).first_or_404()
    print(current_user.id, org.user_id)
    if current_user.id != org.user_id and current_user not in org.get_staff():
        abort(404)
    return render_template('organisations/org_operations.html', op='home', org=org)


@organisations.route('/add/new/', methods=['GET', 'POST'])
@login_required
def create_org():
    form = OrganisationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = images.save(request.files['logo'])
            image_url = images.url(image_filename)
            org = Organisation(
                user_id=current_user.id,
                image_filename=image_filename,
                image_url=image_url,
                org_name=form.org_name.data,
                org_industry=form.org_industry.data,
                org_short_description=form.org_short_description.data,
                org_website=form.org_website.data,
                org_city=form.org_city.data,
                org_state=form.org_state.data,
                org_country=form.org_country.data,
                org_description=form.org_description.data
            )
            db.session.add(org)
            db.session.commit()
            flash('Data added!', 'success')
            logo = Organisation.query.filter(Organisation.logos).first()
            if logo is None:
                return redirect(url_for('organisations.logo_upload'))
            return redirect(url_for('organisations.org_home'))
        else:
            flash('Error! Data was not added.', 'error')
    return render_template('organisations/create_org.html', form=form)


@organisations.route('/<int:org_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_org(org_id):
    org = Organisation.query.filter(Organisation.user == current_user).filter_by(id=org_id).first_or_404()
    form = OrganisationForm(obj=org)
    if request.method == 'POST':
        if form.validate_on_submit():
            org.org_name = form.org_name.data,
            org.org_industry = form.org_industry.data,
            org.org_website = form.org_website.data,
            org.org_city = form.org_city.data,
            org.org_state = form.org_state.data,
            org.org_country = form.org_country.data,
            org.org_description = form.org_description.data
            if request.files['logo']:
                image_filename = images.save(request.files['logo'])
                image_url = images.url(image_filename)
                org.image_filename = image_filename
                org.image_url = image_url
            db.session.add(org)
            db.session.commit()
            flash('Data edited!', 'success')
            return redirect(url_for('organisations.org_home'))
        else:
            flash('Error! Data was not added.', 'error')
    return render_template('organisations/create_org.html', form=form, org=org)


@organisations.route('/<org_id>/list_staff', methods=['Get', 'POST'])
@login_required
def list_staff(org_id):
    org = Organisation.query.filter_by(id=org_id).first_or_404()
    if current_user.id != org.user_id and current_user not in org.get_staff():
        abort(404)
    staff = org.get_staff()
    return render_template('organisations/list_staff.html', staff=staff, org=org)


@organisations.route('/org/<org_id>/view/')
def org_view(org_id):
    """Provide HTML page with all details on an organisation profile """
    org_detail = None
    try:
        org_detail = Organisation.query.filter_by(id=org_id).first()

    except IndexError:
        pass

    if org_detail is not None:
        return render_template('organisations/org_view.html', org_detail=org_detail, org=org_detail)


    elif org_detail == None:
        return redirect(url_for('main.create_org'))

    else:
        abort(404)




@organisations.route('/logo/upload', methods=['GET', 'POST'])
@login_required
def logo_upload():
    ''' check if logo already exist, if it does, send to homepage. Avoid duplicate upload here'''
    check_logo_exist = db.session.query(Logo).filter(Logo.organisation_id == Organisation.id).count()
    if check_logo_exist >= 1:
        return redirect(url_for('main.index'))
    form = LogoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = images.save(request.files['logo'])
            image_url = images.url(image_filename)
            owner_organisation = db.session.query(Organisation).filter_by(user_id=current_user.id).first()
            logo = Logo(
                image_filename=image_filename,
                image_url=image_url,
                owner_organisation=owner_organisation.org_name,
                organisation_id=owner_organisation.id
            )
            db.session.add(logo)
            db.session.commit()
            flash("Image saved.")
            return redirect(url_for('organisations.org_home'))
        else:
            flash('ERROR! Photo was not saved.', 'error')
    return render_template('organisations/upload.html', form=form)


@organisations.route('/<org_id>/invite-staff', methods=['GET', 'POST'])
@login_required
def invite_user(org_id):
    org = Organisation.query.filter_by(user_id=current_user.id).filter_by(id=org_id).first_or_404()
    form = InviteUserForm()
    if form.validate_on_submit():
        invited_by = db.session.query(Organisation).filter_by(user_id=current_user.id).first()
        user = User(
            invited_by=invited_by.org_name,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user.id,
            invited_by=invited_by,
            invite_link=invite_link,
        )
        staff = OrgStaff(user_id=user.id, invited_by=current_user.id, org_id=org_id)
        db.session.add(staff)
        db.session.commit()
        flash('User {} successfully invited'.format(user.full_name),
              'form-success')
        return redirect(url_for('organisations.org_home'))
    return render_template('organisations/new_user.html', form=form, org=org)
