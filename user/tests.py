from django.test import TestCase

# Create your tests here.

from xsadmin import wsgi

from user.models import User


def create_super_user():
    User.objects.create_superuser(username='alishtory',email='alishtory@xsadmin.com',password='alishtory',
                                  port=2312)


if __name__=='__main__':
    create_super_user()