#用户管理服务
USER_HOST = 'auth.ngrok.natapp.cn'
USER_URI= 'http://%s/api/v1.0/users' % USER_HOST


#企业服务
ENTERPRISE_HOST = '114.55.3.224:6001'
ENTERPRISE_URI= 'http://%s/service/api/v1/enp/user/%%d' % ENTERPRISE_HOST

#注册服务
REGISTRATION_HOST = 'dev.jyx365.top:9081'
REGISTRATION_URI = 'http://%s/register?user_id=%%d&next=%%s' % REGISTRATION_HOST


