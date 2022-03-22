
from flask import Flask, render_template, session, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap
from flask_script import Shell, Manager

import requests as r
from  oauthlib import oauth2 
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import webbrowser
import os

load_dotenv()


app = Flask(__name__)
bootstrap = Bootstrap(app)
oauth = OAuth(app)
manager = Manager(app)

app.config['SECRET_KEY'] = os.environ('SECRET_KEY')

def make_shell_context():
    return dict (app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))

oauth.register(
    name='thingiverse',
    client_id= os.environ['CLIENT_ID'],
    client_secret= os.environ['CLIENT_SECRET'],
    access_token_url='https://www.thingiverse.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.thingiverse.com/login/oauth/authorize',
    authorize_params={'response_type':'token'},
    api_base_url='https://api.thingiverse.com/',
    client_kwargs=None,
)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.thingiverse.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():

    return redirect(url_for('index', _external=True))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('auth')

class SubmitForm(FlaskForm):
    login = SubmitField(label='login')

class EnterForm(FlaskForm):
    name = StringField('Enter access token')
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    name = StringField('Enter search category')
    submit = SubmitField('Search')

def get_search_terms(search_term,access_token):
    api_base = "https://api.thingiverse.com/search/"
    full_url = api_base + '{' + search_term + '}' + '?access_token=' + access_token

    search_response = request.post(full_url)


@app.route('/search', methods=['GET','POST'])
def Search():

    search = SearchForm()

    if request.method == "POST":
        get_search_terms(search_term,access_token)

    return render_template('search.html', search = search)

@app.route('/', methods=['GET','POST'])
def index():

    thing_auth = r'https://www.thingiverse.com/login/oauth/authorize'
    response_type = 'token'
    redirect_u = request.base_url

    submit = SubmitForm()
    enter_form = EnterForm()

    if request.method == "POST":

        if request.form.get('login'):

            return redirect('/login')

        if request.form.get('submit'):
            
             return redirect('/search')


    return render_template('index.html', submit = submit, enter=enter_form)



if __name__ == '__main__':



    app.run()


    #token = open_authorisation_page(thing_auth, response_type)

    


