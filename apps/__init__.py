#!flask/bin/python
from flask import Flask

from flask.ext.login import LoginManager
import os
from flask_oauthlib.client import OAuth
from config import WORK_ENV
# from flask.ext.cors import CORS
os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'

app = Flask(__name__,static_folder='prod')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
#lm.session_protection = 'strong'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

oauth = OAuth(app)
oauth_service = oauth.remote_app('wx_web_service',app_key = 'WX_WEB_SERVICE')
# CORS(app)
from sdk.user_api import UserApi
user_api = UserApi(oauth_service)
from sdk.enp_api import EnpApi
enp_api = EnpApi(oauth_service)
from apps import app

from apps import auth
from apps import services_init
from apps import health_check
