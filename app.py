from flask import Flask, render_template, session, url_for, redirect
from authlib.integrations.flask_client import OAuth
from flask.cli import load_dotenv
from os import environ
import peewee
from playhouse.flask_utils import FlaskDB

orm = FlaskDB(
    database='sqlite:///ameth.db',
    excluded_routes=('auth_consent'))

class Member(orm.Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.TextField()

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    assert load_dotenv()
    
    app.secret_key = environ['AMETH_SECRET_KEY']
    
    orm.init_app(app)
    with orm.database:
        orm.database.create_tables([Member])
    
    oauth.init_app(app)
    oauth.register(
        name='osu',
        client_id=environ['OSU_CLIENT_ID'],
        client_secret=environ['OSU_CLIENT_SECRET'],
        access_token_url='https://osu.ppy.sh/oauth/token',
        authorize_url='https://osu.ppy.sh/oauth/authorize',
        api_base_url='https://osu.ppy.sh/api/v2/',
    )
    
    return app

app = create_app()
db = orm.database

@app.route('/')
def root():
    if session.get('osu'):
        return render_template('manage.html', username=session['osu']['username'])
    else:
        return render_template('welcome.html')

@app.route('/consent')
def auth_consent():
    osu_client = oauth.create_client('osu')
    return osu_client.authorize_redirect(url_for('auth_process', _external=True))

@app.route('/authorize')
def auth_process():
    token = oauth.osu.authorize_access_token()
    response = oauth.osu.get('me', token=token)
    response.raise_for_status()
    me = response.json()
    
    with db.atomic():
        session['osu'] = {
            'username': me['username'],
            'id': me['id']
        }
        
        if Member.get_or_none(Member.id == session['osu']['id']):
            return redirect(url_for('root')) # will render account dash if a session is active
        else:
            Member.create(
                id=session['osu']['id'],
                username=session['osu']['username']
            )
            return render_template('success.html', 
                                    username=session['osu']['username'])

