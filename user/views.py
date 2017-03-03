from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout,update_session_auth_hash
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.core.urlresolvers import reverse,reverse_lazy


# Create your views here.

def logout(request):
    auth_logout(request)
    return redirect('home:login')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user/dashboard.html'

class ProfileView(LoginRequiredMixin, UpdateView):

    form_class = ProfileForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_wapper_class'] = 'col-xs-6 col-sm-5 col-md-4'
        context['page_title'] = '我的基本信息'
        return context

    def get_success_url(self):
        return reverse('user:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswdView(LoginRequiredMixin, UpdateView):

    form_class = PasswdForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_wapper_class'] = 'col-xs-6 col-sm-5 col-md-4'
        context['page_title'] = '修改Shadowsocks连接密码'
        return context

    def get_success_url(self):
        return reverse('user:passwd')

    def get_object(self, queryset=None):
        return self.request.user

class PasswordView(LoginRequiredMixin, UpdateView):

    form_class = PasswordForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('user:password')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_wapper_class'] = 'col-xs-6 col-sm-5 col-md-4'
        context['page_title'] = '修改用户登录密码'
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form=form)
        update_session_auth_hash(request=self.request, user=form.instance)
        return response

class NodeListView(LoginRequiredMixin, ListView):

    template_name = 'user/nodes.html'
    model = Node
    context_object_name = 'nodeLists'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset



