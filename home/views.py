from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth import login,logout as auth_logout
from django.contrib.auth.views import _get_login_redirect_url
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import *
from django.conf import settings
import datetime
from . import utils

# Create your views here.

class IndexView(TemplateView):
    template_name = 'home/index.html'

class DownloadView(TemplateView):
    template_name = 'home/download.html'

class AboutView(TemplateView):
    template_name = 'user/../templates/home/forgot_password.html'

REDIRECT_FIELD_NAME = 'next'

class BaseAuthedRedirectFormView(FormView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == request.path:
                raise ValueError('LOGIN_REDIRECT_URL配置错误，不能指向login的URL，否则会无限重定向')
            return HttpResponseRedirect(redirect_to)
        return super(BaseAuthedRedirectFormView,self).dispatch(request, args, kwargs)

class LoginView(BaseAuthedRedirectFormView):

    template_name = 'home/login.html'
    form_class = LoginForm

    def get_success_url(self):
        request = self.request
        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        redirect_to = _get_login_redirect_url(request,redirect_to)
        return redirect_to

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super(LoginView,self).form_valid(form)


class RegisterView(BaseAuthedRedirectFormView):

    form_class = RegisterForm
    template_name = 'home/register.html'

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        #验证无误，注册用户，废除邀请码
        code = InviteCode.objects.get(code__exact=form.cleaned_data.get('invite_code'))
        ip = utils.get_remote_ip(self.request)
        now = datetime.datetime.now()
        extra_fields = {
            'transfer_enable': code.traffic,
            'reg_ip': ip,
            'last_login_ip': ip,
            'this_login_ip': ip,
        }
        user = User.objects.create_user(username= form.cleaned_data['username'],
                email= form.cleaned_data['email'],password= form.cleaned_data['password'], **extra_fields)

        code.enable = False
        code.used_user = user
        code.used_time = now
        code.save()
        login(request=self.request,user=user)
        return super(RegisterView,self).form_valid(form)

