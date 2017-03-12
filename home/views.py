from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth import login,logout as auth_logout
from django.contrib.auth.views import _get_login_redirect_url
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import *
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from . import utils
from django.http import HttpResponse,HttpResponseForbidden
from geetest import GeetestLib
from django.core.exceptions import PermissionDenied
from user import utils as UserUtils
from user.models import Post
from django.http.response import Http404
from django.db.models import Q
from password_reset.views import Recover

# Create your views here.

REDIRECT_FIELD_NAME = 'next'

class AuthedRedirectMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == request.path:
                raise ValueError('LOGIN_REDIRECT_URL配置错误，不能指向login的URL，否则会无限重定向')
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class GeeCaptchaValidateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            gt = GeetestLib(settings.GEE_CAPTCHA_ID, settings.GEE_PRIVATE_KEY)
            challenge = request.POST.get(gt.FN_CHALLENGE, '')
            validate = request.POST.get(gt.FN_VALIDATE, '')
            seccode = request.POST.get(gt.FN_SECCODE, '')
            status = request.session.get(gt.GT_STATUS_SESSION_KEY)
            user_id = request.session.get("gee_user_id")
            if status:
                result = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                result = gt.failback_validate(challenge, validate, seccode)
            if not result:
                raise PermissionDenied('请正确滑动解锁')
        return super().dispatch(request, *args, **kwargs)



class LoginView(AuthedRedirectMixin, GeeCaptchaValidateMixin, FormView):

    template_name = 'home/login.html'
    form_class = LoginForm

    def get_success_url(self):
        request = self.request
        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        redirect_to = _get_login_redirect_url(request,redirect_to)
        return redirect_to

    def form_valid(self, form):
        login(self.request, form.user_cache)
        if not form.cleaned_data.get('remember'):
            self.request.session.set_expiry(0)
        return super(LoginView,self).form_valid(form)


class RegisterView(AuthedRedirectMixin, GeeCaptchaValidateMixin, FormView):

    form_class = RegisterForm
    template_name = 'home/register.html'

    def get_initial(self):
        inital = super().get_initial()
        inital['invite_code'] = self.request.GET.get('invite_code','')
        return inital

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        #验证无误，注册用户，废除邀请码
        code = InviteCode.objects.get(code__exact=form.cleaned_data.get('invite_code'))
        ip = utils.get_remote_ip(self.request)
        now = timezone.now()
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


class GeeCaptchaView(View):

    def post(self, request, *args, **kwargs):
        gee_user_id = request.session.get('gee_user_id')
        if gee_user_id is None:
            gee_user_id = UserUtils.gen_api_key()
            request.session["gee_user_id"] = gee_user_id
        gt = GeetestLib(settings.GEE_CAPTCHA_ID, settings.GEE_PRIVATE_KEY)
        status = gt.pre_process(gee_user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status

        response_str = gt.get_response_str()
        return HttpResponse(response_str, content_type='application/json')

class InviteCodeView(TemplateView):
    template_name = 'home/code.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        delay = timedelta(minutes=10)
        context['codes'] = InviteCode.objects.filter(
            (Q(type=InviteCode.TYPE_DEFAULT)|
             (Q(type=InviteCode.TYPE_TIMING)&Q(show_time__gte=now))
             )&(Q(enable=True)|Q(used_time=None)|Q(used_time__range=(now-delay,now+delay)))).order_by('-enable','-id')[:30]
        return context

class PostPageView(TemplateView):

    page_temp_list = ('index', 'about', 'download', 'tos')
    page = None
    default_slug = 'index'
    current_slug = default_slug

    def get_template_names(self):
        if self.page is None:
            if self.current_slug in self.page_temp_list:
                return 'home/%s.html' % self.current_slug
            else:
                raise Http404('No That Page!')
        else:
            return 'home/post_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.current_slug = self.kwargs.get('slug', self.default_slug)
        try:
            page = Post.objects.get(slug__iexact= self.current_slug, content_type= 'PAGE', status= 'PUBLISHED')
            self.page = page
            context['page'] = page
        except Post.DoesNotExist or Post.MultipleObjectsReturned:
            pass
        return context

class MyRecover(GeeCaptchaValidateMixin, Recover):

    pass