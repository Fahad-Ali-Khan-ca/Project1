from flask import Flask, render_template, url_for, request, redirect,flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
import babel
from forms import RegistrationForm,LoginForm, newForm
import email_validator

app = Flask(__name__)

app.config['SECRET_KEY']='f3ed7d6ffe91ef8f3f033c7a21482a47'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project1.db'



db = SQLAlchemy(app)


class Bookit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    Venue=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime)
    def _repr_(self):
        return '<Name %r>' % self.id

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Project1.db'
    db.init_app(app)
    return app

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')

    def __init__(self, name, address, city, state, phone,):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    def short(self):
        return{
            'id':self.id,
            'name':self.name,
        }
    
    def long(self):
        print(self)
        return{
            'id' :self.id,
            'name' :self.name,
            'city' : self.city,
            'state' :self.state,
        }   

class Show(db.Model):
  __tablename__='shows'
  id=db.Column(db.Integer, primary_key=True)

  artist_id=db.Column(db.Integer,db.ForeignKey('Artist.id'), nullable=False)
  venue_id=db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)
  start_time=db.Column(db.String(),nullable=False)

  def __init__(self, venue_id,artist_id,start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def detail(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name' :self.Venue.name,
            'artist_id' :self.artist_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time
        }

  def artist_details(self):
        return{
            'artist_id' :self.venue_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time

        }
 
    
  def venue_details(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name' :self.Venue.name,
            'venue_image_link' :self.Venue.image_link,
            'start_time' :self.start_time
            
        }
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    booking_venue = db.Column(db.Boolean, default=False)
    booking_description = db.Column(db.String(120), default=' ')
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __init__(self, name, genres, city, state, phone, image_link, website, facebook_link,
                 booking_venue=False, booking_description=""):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.booking_description = booking_description
        self.image_link = image_link
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def short(self):
        return{
            'id': self.id,
            'name':self.name,
        }
    
    def details(self):
        return{
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state':self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'booking_venue': self.booking_venue,
            'booking_description': self.booking_description,
            'image_link': self.image_link,

        }

with app.app_context():
    db.create_all()


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/Concert')
def Concert():
  return render_template('Venue_owner.html')

@app.route('/artists')
def Artists():
    return render_template('index.html')

@app.route('/shows')
def Shows():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/Concert/create", methods=['GET', 'POST'])
def new():
    form = newForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('new_venue.html', title='newForm', form=form)


#AERAF MAKE HTML Update your Venue
@app.route("/update")
def update():
    return render_template('')

@app.route("/commercial")
def commercial():
    return render_template('')

if __name__ == "__main__":
    app.run(debug=True)
