from django.test import TestCase

# Create your tests here.


class AMixin():
    def say(self):
        print('AMixin')
        super().say()

class B():
    def say(self):
        print('BMixin')
        super().say()

class CMixin():
    def say(self):
        print('CMixin')
        #super().say()

class User(AMixin,B,CMixin):

    def say(self):
        print('User')
        super().say()


u = User()
u.say()