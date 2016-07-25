# -*- coding:utf-8 -*-
import requests, json
from flask import render_template, flash, redirect, request, jsonify,url_for
from resources import *
from apps import app
# USER_URI= 'http://120.27.150.13:6053/api/v1.0/users'
# REGISTRATION_URI = 'http://120.27.150.13:6053/api/v1.0/registration'
class UserApi:
    host = 'localhost:5051'
    user_baseurl = USER_URI
    headers = {'content-type':'application/json'}

    _oauth_client = None

    def __init__(self,oauth_client=None):
        self._oauth_client = oauth_client

    def get_users( self,id = None, openid = None, mobile = None, name = None):
        payload = {}
        if id is not None:
            payload['id'] = int(id)
        if openid:
            payload['openid'] = openid
        if mobile:
            payload['mobile'] = mobile
        if name:
            payload['name'] = name
        print(payload)
        url=self.user_baseurl
        r=self._oauth_client.get(url,data=payload)
        if r.status != 200 or not r.data or not r.data['users']:
            print(r.data)
            return None
        return r.data['users']


    def add_user(self, openid):
        url = self.user_baseurl
        headers = {'content-type': 'application/json'}
        payload = {'openid':openid}
        r=self._oauth_client.post(url,content_type='application/json',
                                      data=json.dumps(payload))
        if r.status != 201:
            return None
        if not r.data or not 'user' in r.data :
            return None
        return r.data['user']

    def update_user(self, id, mobile = None, name = None):
        payload = {}
        if mobile:
            payload['mobile'] = mobile
        if name:
            payload['name'] = name
        url = '/api/v1.0/users/' + str(id)
        r = self._oauth_client.put(url,
                content_type = 'application/json',
                data = json.dumps(payload))
        if r.status != 200:
            return None
        if not r.data or not 'user' in r.data :
            return None
        return r.data['user']

    def update_current_user(self, email=None, desc=None, portrait_uri=None):
        payload = {}
        if email:
            payload['email'] = email
        if desc:
            payload['desc'] = desc
        if portrait_uri:
            payload['portrait_uri'] = portrait_uri
        url = '/api/v1.0/users/current'
        r = self._oauth_client.put(url,
                content_type = 'application/json',
                data = json.dumps(payload))
        if r.status != 200:
            return None
        if not r.data or not 'user' in r.data :
            return None
        return r.data['user']



    def register(self, user_id, mobile):
        '''用户注册接口'''
        #TODO:应该直接调用OAuth服务的注册接口

        name = None
        enterprise_id = None

        payload = {'user_id' : user_id, 'mobile' : mobile}
        r = self._oauth_client.post(ACTIVITY_REGISTRATION_URI,
                content_type='application/json',
                data=json.dumps(payload)
                )
        print('resp:',r.data)
        participators = None
        user = None

        if r.status == 201 :
            if  r.data and 'participators' in r.data:
                participators = r.data['participators']
                name = participators[0]['name']

        payload = {'userId':user_id, 'phone':mobile}
        r = self._oauth_client.post(ENTERPRISE_REGISTRATION_URI,
                content_type = 'application/json',
                data = json.dumps(payload)
                )

        print('enterprise resp:',r.data)
        if r.status == 200:
            if r.data:
                enterprise_id = r.data['orgId']
                name = r.data['name']


        payload = {'mobile':mobile, 'enterprise_id':enterprise_id, 'name':name}
        print(payload)
        r = self._oauth_client.put('/api/v1.0/users/%d'%user_id,
                content_type = 'application/json',
                data = json.dumps(payload)
                )
        print('update_user:',r.data)
        if r.status != 200:
            return None

        return {'participators':participators,'user':user}

    # def register(self, user_id, mobile ):
        # payload = {'user_id' : user_id, 'mobile' : mobile}
        # print('access_token:',self._tokengetter())
        # headers = self.headers
        # headers['Authorization']='bearer '+ ' '.join(self._tokengetter())
        # r = requests.post(
                # REGISTRATION_URI,
                # data = json.dumps(payload),
                # headers = headers)
        # if r.status_code != 201:
            # print(r.json)
            # return None
        # if not r.json() or not 'participators' in r.json():
            # return None
        # return r.json()['participators']

