from django.test import TestCase

# Create your tests here.


class AMixin():
    def say(self):
        print('AMixin')

class B():
    def say(self):
        print('BMixin')

class CMixin():
    def say(self):
        print('CMixin')

class User(AMixin,B,CMixin):
    pass
    # def say(self):
    #     print('User')
    #     super(AMixin,self).say()


u = User()
u.say()