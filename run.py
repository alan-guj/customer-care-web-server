#!flask/bin/python
from apps import app
from apps.services_init import services_resources_init

app.config.from_object('config')
if __name__ == '__main__':
    rc=services_resources_init()
    if rc != True:
        print("run error, services_resources_init error")
    else:
        app.run(debug=True, threaded=True, host='0.0.0.0', port=7053)
