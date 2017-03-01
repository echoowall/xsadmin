from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth import login,logout as auth_logout
from django.contrib.auth.views import _get_login_redirect_url
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Create your views here.
class BaseHomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseHomeView, self).get_context_data(**kwargs)
        #context['']
        return context

class IndexView(BaseHomeView):
    template_name = 'home/index.html'

class DownloadView(BaseHomeView):
    template_name = 'home/download.html'

class AboutView(BaseHomeView):
    template_name = 'user/forgot_password.html'

from .forms import *

REDIRECT_FIELD_NAME = 'next'

class LoginView(BaseHomeView):

    redirect_authenticated_user = True
    template_name = 'user/login.html'

    def get_redirect_to(self,request):
        redirect_to = self.request.POST.get(REDIRECT_FIELD_NAME, self.request.GET.get(REDIRECT_FIELD_NAME, ''))
        return redirect_to

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            redirect_to = _get_login_redirect_url(request, self.get_redirect_to(request))
            if redirect_to == request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super(LoginView,self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            form = LoginForm(self.request.POST)
        else:
            form = LoginForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        if form.is_valid():
            login(request, form.user_cache)
            redirect_to = _get_login_redirect_url(request,self.get_redirect_to(request))
            return HttpResponseRedirect(redirect_to)
        print(form.errors)
        return self.render_to_response(context)

def logout(request):
    auth_logout(request)
    return redirect('home:login')
