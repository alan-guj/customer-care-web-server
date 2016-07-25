# -*- coding:utf-8 -*-
import requests, json
from flask import render_template, flash, redirect, request, jsonify,url_for
from resources import *
from apps import app
# USER_URI= 'http://120.27.150.13:6053/api/v1.0/users'
# REGISTRATION_URI = 'http://120.27.150.13:6053/api/v1.0/registration'
class EnpApi:
    baseurl = ENTERPRISE_URI
    headers = {'content-type':'application/json'}

    _oauth_client = None

    def __init__(self,oauth_client=None):
        self._oauth_client = oauth_client

    def get_enp_user(self,id):
        url=self.baseurl % id
        print(url)
        r=self._oauth_client.get(url)
        if r.status != 200 or not r.data :
            print(r.data)
            return None
        return r.data


