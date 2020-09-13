from flask_ckeditor import CKEditorField
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    DecimalField,
    FloatField,
    FileField,
    BooleanField,
    MultipleFileField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    Required,
    Optional,
)
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional
from wtforms_alchemy import Unique, ModelForm, model_form_factory

from app import db
from app.models import *

images = UploadSet('images', IMAGES)
BaseModelForm = model_form_factory(FlaskForm)

#####Payment Forms Starts #####

class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class OrgStaffForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(OrgStaffForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


#####User Forms Ends #####

#####Blog Forms Starts #####
class BlogCategoryForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    order = IntegerField('Order', validators=[InputRequired()])
    is_featured = BooleanField("Is Featured ?")
    submit = SubmitField('Submit')


class BlogTagForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class BlogNewsLetterForm(BaseModelForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email(), Unique(BlogNewsLetter.email)])
    submit = SubmitField('Submit')


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    text = CKEditorField('Body', validators=[InputRequired()])
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    categories = QuerySelectMultipleField(
        'Categories',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogCategory).order_by('order'))
    tags = QuerySelectMultipleField(
        'Tags',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(BlogTag).order_by('created_at'))
    newsletter = BooleanField('Send Announcement To Subscribers.')
    all_users = BooleanField('Send Announcement To All Users.')

    submit = SubmitField('Submit')

#####Forms Ends #####

class SocialForm(FlaskForm):
    twitter_name = StringField('Twitter accname only')
    facebook_name = StringField('Facebook pagename only')
    instagram_name = StringField('Instagram username only')
    tiktok_name = StringField('Tiktok username only')
    linkedin_name = StringField('Linkedin pagename only')
    snap_chat_name = StringField('Snap chat username only')
    youtube = StringField('Youtube page name only')
    submit = SubmitField('Submit')

class OrganisationForm(FlaskForm):
    org_name = StringField('Organisation name', validators=[InputRequired(), Length(1, 64)])
    #logo = FileField('Organisation Logo', validators=[FileAllowed(images, 'Images only!')])
    #logo = FileField('Organisation Logo', validators=[Required(), FileAllowed(images, 'Images only!')])
    org_industry = SelectField(u'Select Industry', choices=[('Small Business', 'Small Business'),
                                                            ('Church','Church'), ('Restaurant','Restaurant')])
    org_short_description = StringField('One Line of Text', [Length(max=255)])
    org_website = StringField('Website', [Length(max=255)])
    org_city = StringField('City', [Length(max=255)])
    org_state = StringField('State or Region', [Length(max=255)])
    org_country = SelectField(u'Select Country', choices=[

        ('Afganistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antigua & Barbuda', 'Antigua & Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bermuda', 'Bermuda'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bonaire', 'Bonaire'),
        ('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('British Indian Ocean Ter', 'British Indian Ocean Ter'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Canary Islands', 'Canary Islands'),
        ('Cape Verde', 'Cape Verde'),
        ('Cayman Islands', 'Cayman Islands'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Channel Islands', 'Channel Islands'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Christmas Island', 'Christmas Island'),
        ('Cocos Island', 'Cocos Island'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Costa Rica', 'Costa Rica'),
        ('Cote DIvoire', 'Cote DIvoire'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Curaco', 'Curacao'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic', 'Czech Republic'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor', 'East Timor'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Falkland Islands', 'Falkland Islands'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('French Guiana', 'French Guiana'),
        ('French Polynesia', 'French Polynesia'),
        ('French Southern Ter', 'French Southern Ter'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Great Britain', 'Great Britain'),
        ('Greece', 'Greece'),
        ('Greenland', 'Greenland'),
        ('Grenada', 'Grenada'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Hawaii', 'Hawaii'),
        ('Honduras', 'Honduras'),
        ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('Indonesia', 'Indonesia'),
        ('India', 'India'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Isle of Man', 'Isle of Man'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea North', 'Korea North'),
        ('Korea Sout', 'Korea South'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Macau', 'Macau'),
        ('Macedonia', 'Macedonia'),
        ('Madagascar', 'Madagascar'),
        ('Malaysia', 'Malaysia'),
        ('Malawi', 'Malawi'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Martinique', 'Martinique'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'),
        ('Mexico', 'Mexico'),
        ('Midway Islands', 'Midway Islands'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montserrat', 'Montserrat'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar', 'Myanmar'),
        ('Nambia', 'Nambia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherland Antilles', 'Netherland Antilles'),
        ('Netherlands', 'Netherlands (Holland, Europe)'),
        ('Nevis', 'Nevis'),
        ('New Caledonia', 'New Caledonia'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'),
        ('Norfolk Island', 'Norfolk Island'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau Island', 'Palau Island'),
        ('Palestine', 'Palestine'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Phillipines', 'Philippines'),
        ('Pitcairn Island', 'Pitcairn Island'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Qatar', 'Qatar'),
        ('Republic of Montenegro', 'Republic of Montenegro'),
        ('Republic of Serbia', 'Republic of Serbia'),
        ('Reunion', 'Reunion'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('St Barthelemy', 'St Barthelemy'),
        ('St Eustatius', 'St Eustatius'),
        ('St Helena', 'St Helena'),
        ('St Kitts-Nevis', 'St Kitts-Nevis'),
        ('St Lucia', 'St Lucia'),
        ('St Maarten', 'St Maarten'),
        ('St Pierre & Miquelon', 'St Pierre & Miquelon'),
        ('St Vincent & Grenadines', 'St Vincent & Grenadines'),
        ('Saipan', 'Saipan'),
        ('Samoa', 'Samoa'),
        ('Samoa American', 'Samoa American'),
        ('San Marino', 'San Marino'),
        ('Sao Tome & Principe', 'Sao Tome & Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Tahiti', 'Tahiti'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'),
        ('Trinidad & Tobago', 'Trinidad & Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Turks & Caicos Is', 'Turks & Caicos Is'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('United Kingdom', 'United Kingdom'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Erimates', 'United Arab Emirates'),
        ('United States of America', 'United States of America'),
        ('Uraguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City State', 'Vatican City State'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands (Brit)', 'Virgin Islands (Brit)'),
        ('Virgin Islands (USA)', 'Virgin Islands (USA)'),
        ('Wake Island', 'Wake Island'),
        ('Wallis & Futana Is', 'Wallis & Futana Is'),
        ('Yemen', 'Yemen'),
        ('Zaire', 'Zaire'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe')])
    org_website = StringField('www.example.com', [Length(max=255)])
    org_description = TextAreaField('Description', [Required()])
    submit = SubmitField('Submit')
    
class AboutForm(FlaskForm):


    about_us_title = StringField('About us title text')
    key_information_title_one = StringField('Second line title text')
    key_information_title_two = StringField('Third line title text')
    key_information_title_three = StringField('Fourth line title text')
 
    key_information_description_one = StringField('About us title description text')
    key_information_description_two = StringField('Second line title description text')
    key_information_description_three = StringField('Third line title description text')
 
    key_information_icon_one = StringField('Icon One')
    key_information_icon_two = StringField('Icon Two')
    key_information_icon_three = StringField('Icon Three ')

    key_information_numbers_one = StringField(' Number of clients E.g 232')
    key_information_numbers_two = StringField('Number of projects E.g 532')
    key_information_numbers_three = StringField('Number of support E.g 1,463 ')
    key_information_numbers_four = StringField('Number of workers E.g 20')
 
    key_information_numbers_description_one = StringField('E.g Clients')
    key_information_numbers_description_two = StringField('E.g Projects')
    key_information_numbers_description_three = StringField('E.g Hours of support')
    key_information_numbers_description_four = StringField('E.g Employees') 
    
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class HtmlForm(FlaskForm):
    block_content_one = TextAreaField('Description')
    html_code_one = TextAreaField('Insert raw html')
    html_code_two = TextAreaField('Insert raw html')
    html_code_three = TextAreaField('Insert raw html')
    html_code_four = TextAreaField('Insert raw html')
    submit = SubmitField('Submit')


class Call2actionForm(FlaskForm):
    description = StringField('Call to action text')
    call2action_url = TextAreaField('Call to action url')
    submit = SubmitField('Submit')


#####Frontend Forms Starts #####
class PortfolioForm(FlaskForm):
    portfolio_name = StringField('Example Mercedes or Bicycle', validators=[InputRequired(), Length(1, 25)])
    portfolio_title = StringField('Automobiles', validators=[InputRequired(), Length(1, 50)])
    portfolio_description = TextAreaField('Website description', validators=[InputRequired(), Length(1, 180)])
 
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')

class TeamForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired(), Length(1, 25)])
    job_title = StringField('Job title', validators=[InputRequired(), Length(1, 50)])
    job_description = StringField('Job description', validators=[InputRequired(), Length(1, 180)])
    team_member_twitter = StringField('e.g @teammember')
    team_member_facebook = StringField('e.g JohnPaul')
    team_member_linkedin = StringField('Full Name on Linkedin')
    team_member_instagram = StringField('@username')
    image = FileField('Image', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')
 
#####Frontend Forms Starts #####
class LandingSettingForm(FlaskForm):
    site_name = StringField('Site Name e.g bookstore.ng', validators=[InputRequired(), Length(1, 128)])
    title = StringField('Website Title', validators=[InputRequired(), Length(1, 128)])
    description = StringField('Website description', validators=[InputRequired(), Length(1, 180)])
    twitter_name = StringField('Twitter accname only')
    facebook_name = StringField('Facebook pagename only')
    instagram_name = StringField('Instagram username only')
    tiktok_name = StringField('Tiktok username only')
    linkedin_name = StringField('Linkedin pagename only')
    snap_chat_name = StringField('Snap chat username only')
    youtube = StringField('Youtube page name only')
    blog = StringField('e.g blog')
    about = StringField('e.g about')
    contact = StringField('e.g contact')
    faq = StringField('e.g faq')
    
    logo = FileField('Logo', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    #images = MultipleFileField('Images', validators=[InputRequired(), FileAllowed(images, 'Images only!')])
    h1 = StringField('H1 text', validators=[InputRequired(), Length(1, 180)])
    h2 = StringField('H2 Text')
    h3 = StringField('H3 Text')
    h4 = StringField('H4 Text')
    h5 = StringField('H5 Text')
  
    featured_title_one = StringField('e.g Fast delivery')
    featured_title_one_text = StringField('Write about 90 words')
    featured_title_one_icon = StringField('e.g fa-truck')
    featured_title_two = StringField('e.g Creative Strategy')
    featured_title_two_text = StringField('Write about 90 words')
    featured_title_two_icon = StringField('e.g fa-landmark')
    featured_title_three = StringField('e.g High secured')
    featured_title_three_text = StringField('Write about 90 words')
    featured_title_three_icon = StringField('e.g fa-lock')
    
    google_analytics_id = StringField('Google Analytics ID')
    other_tracking_analytics_one = StringField('Insert Analytics Script')
    other_tracking_analytics_two = StringField('Insert Analytics Script')
    other_tracking_analytics_three = StringField('Insert Analytics Script')
    other_tracking_analytics_four = StringField('Insert Analytics Script')
    block_content_one = TextAreaField('Description')
    html_code_one = TextAreaField('Insert raw html')
    html_code_two = TextAreaField('Insert raw html')
    html_code_three = TextAreaField('Insert raw html')
    html_code_four = TextAreaField('Insert raw html')
    submit = SubmitField('Submit')

class PhotoForm(FlaskForm):

    image = FileField('Image', validators=[Optional(), FileAllowed(images, 'Images only!')])
    file_name = StringField('e.g Favicon')
    submit = SubmitField('Submit')

class OurBrandForm(FlaskForm):
    ### these are brands which we own in house
    
    brand_name_one = StringField('e.g Mediville')
    brand_name_two = StringField('e.g Networkedng')
    brand_name_three = StringField('e.g Intel')
    brand_name_four = StringField('e.g teamsworkspace')
    brand_name_five = StringField('e.g teamsworkspace')
    brand_url_one = StringField('e.g mediville.com')
    brand_url_two = StringField('e.g https://networked.ng')
    brand_url_three = StringField('e.g http://intel.com')
    brand_url_four = StringField('e.g teamsworkspace.com.ng')
    brand_url_five = StringField('e.g https://teamsworkspace.com.ng')
    submit = SubmitField('Submit')

class NewsLinkForm(FlaskForm):
    ### these are news sites that write about us
    
    news_site_one = StringField('e.g CNN')
    news_site_two = StringField('e.g BBC')
    news_site_three = StringField('e.g FoxNews')
    news_site_four = StringField('e.g PunchNews')
    news_site_five = StringField('e.g Vanguard')
    news_url_one = StringField('e.g cnn.com/link_to_news')
    news_url_two = StringField('e.g https://bbc.com/link_to_news')
    news_url_three = StringField('e.g http://foxnews.com/link_to_news')
    news_url_four = StringField('e.g punch.ng/link_to_news')
    news_url_five = StringField('e.g https://vanguard.com/link_to_news')
    submit = SubmitField('Submit')

class ImageForm(FlaskForm):
    logo = FileField('Logo', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')
