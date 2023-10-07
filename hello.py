from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cats are the best'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
  name = StringField('What is your name?', validators=[DataRequired()])
  email = StringField('What is your UofT Email address?', validators=[Email()])
  submit = SubmitField('Submit')
  def validate_email(form, field):
    form.uoftNotValid=False
    if "@" not in field.data:
      raise ValidationError('Please include @ in the email.')
    if "utoronto" not in field.data:
      form.uoftNotValid=True
      raise ValidationError('Please use your UofT email.')


@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    
    old_email = session.get('email')
    if old_email is not None and old_email != form.email.data:
      flash('Looks like you have changed your email!')
    session['email'] = form.email.data
    
    return redirect(url_for('index'))
  return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))
    
@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
  app.run(debug=True)