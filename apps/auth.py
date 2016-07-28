# -*- coding:utf-8 -*-
from apps import app,oauth_service,user_api, enp_api
from flask.ext.login import LoginManager,UserMixin,login_user,current_user,login_required
from flask import render_template, flash, redirect, request, jsonify,url_for, session
from flask import stream_with_context, Response, abort
from flask_oauthlib.client import OAuthException
from apps import lm
import requests, json
from flask.ext.wtf import Form
from wtforms import StringField, RadioField, HiddenField, SelectField

from wtforms.validators import DataRequired
from resources_json import *
from resources import *
import logging
import sys
from .services_init import services

log = logging.getLogger('wx_web_server_auth')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

@oauth_service.tokengetter
def get_token(token=None):
    return session.get('access_token')


class AuthUser(UserMixin):
    id = None
    openid = None
    name = None
    mobile = None
    cur_activity = None
    data = None
    enpinfo = None
    type = 'guest'
    def __init__(self,id,openid, mobile, name, data=None,type=None, enpinfo=None):
        self.id = id
        self.openid = openid
        self.name = name
        self.mobile = mobile
        self.data = data
        self.type = type
        self.enpinfo= enpinfo

@app.route('/testlogin',methods=['POST','GET'])
def test_login():
    return oauth_service.authorize(
            callback = url_for(
                'authorized', next=request.args.get('next'),
                _external = True
                ),
            # user_id = request.args.get('user_id',43),
            )

@app.route('/customer_care/login', methods = ['POST','GET'])
def login():
    '''认证入口'''
    return oauth_service.authorize(
            callback = url_for(
                'authorized', next=request.args.get('next'),_external = True
                ),
            # user_id = request.args.get('user_id',43),
            )

@app.route('/customer_care/authorized', methods = ['POST','GET'])
def authorized():
    '''认证通过回调函数'''
    auth_resp = oauth_service.authorized_response()
    if auth_resp is None:
        return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
                )
    log.debug(auth_resp)
    if isinstance(auth_resp,OAuthException) or not 'access_token' in auth_resp:
        return redirect(url_for('login'))
    session['access_token'] = (auth_resp['access_token'],'')
    session['token'] = auth_resp;
    resp = oauth_service.get('/api/v1.0/users/current', token={'access_token': auth_resp['access_token']})
    log.debug('access_token = %s', session['access_token'])
    log.debug('status=%s,data=%s',resp.status,resp.data)
    if resp.status != 200:
        return '认证失败',404
    user = resp.data['user']

    enpinfo = enp_api.get_enp_user(id=user['id'])

    login_user(AuthUser(id = user['id'], openid = user['openid']\
             , mobile = user['mobile'], name = user['name'],type=user['type'],
             data=user,enpinfo=enpinfo))

    next = request.args.get('next')

    if next is not None and next.startswith('/register'):
        return redirect(next)
    # if not 'mobile' in user or user['mobile'] is None:
    if user['type'] is None or user['type'] == 'guest':
        session['user_id'] =  user['id']
        return redirect(REGISTRATION_URI % (user['id'],next))
    if next is not None:
        return redirect(next)
    return redirect(url_for('customer_care_app'))

# @app.route('/customer_care')
# @login_required
# def customer_care():
    # return render_template(
            # 'customer_care.html',
            # token=session['access_token'][0],
            # web_servers = web_servers,
            # services = services,
            # sys_params = sys_params)


@app.route('/customer_care')
@login_required
def customer_care_app(mode='prod'):
    return render_template(
            'customer_care_app.html',
            token=session['token'],
            web_servers = web_servers,
            services = services,
            sys_params = sys_params,
            oauth_params = oauth_params,
            mode=mode)



@lm.user_loader
def load_user(id):
    print('load_user:%d',id)
    resp = oauth_service.get('/api/v1.0/users/current')
    if resp.status != 200:
        return None
    user = resp.data['user']
    if user['type'] is None or user['type'] == 'guest':
        return None
    print(user)
    enpinfo = enp_api.get_enp_user(id=user['id'])
    print(enpinfo)
    # if not 'mobile' in user or user['mobile'] is None:
        # return None
    return AuthUser(
            id = id,
            openid = user['openid'],
            name = user['name'],
            mobile = user['mobile'],
            type = user['type'],
            data = user,
            enpinfo = enpinfo)


