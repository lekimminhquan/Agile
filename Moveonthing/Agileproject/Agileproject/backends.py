from django.contrib.auth.backends import ModelBackend
from MOT.models import Taikhoan
from django.contrib.auth.hashers import *


class PersonalizedLoginBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, role=None , **kwars):
        try:
            user = Taikhoan.objects.get(username=username)
        except Taikhoan.DoesNotExist:
            return None
        if user.password == password and user.phanquyen == role:
            return user
        else:
            return None

    def get_user(self, user_id):
        #This shall return the user given the id
        from django.contrib.auth.models import AnonymousUser
        try:
            user = Taikhoan.objects.get(matk=user_id)
        except Exception as e:
            user = AnonymousUser()
        return user