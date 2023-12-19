from flask import Flask, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from flask.cli import load_dotenv
from os import environ

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    assert load_dotenv()
    
    app.secret_key = environ['AMETH_SECRET_KEY']
    
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

    session['osu'] = {
        'username': me['username'],
        'id': me['id']
    }
    
    return render_template('success.html', 
                            username=session['osu']['username'])

