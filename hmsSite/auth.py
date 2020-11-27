from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from json import loads
import requests


class PhemeBackend(BaseBackend):
    # passes the username and password to the makers api
    def authenticate(self, request, username:None, password=None):
        post_req = requests.post("https://auth.uwamakers.com/api/login", data = {
                'token':'92D6oxLPUkEVPYr8k7oozEhWeRqvzzbr5ed7FX2l6C48',
                'user':username,
                'pass':password
            })
            # if the request returns successful, need to write custom auth and stuff
        if post_req.status_code == 200:
            text = loads(post_req.text)
            try:
                user = User.objects.get(username=text['user']['username'])
            except User.DoesNotExist:
                user = User(username=username, email=text['user']['email'], first_name=text['user']['firstname'], last_name=text['user']['lastname'])
                user.save()
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

