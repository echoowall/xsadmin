from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout,update_session_auth_hash
from django.shortcuts import redirect,get_object_or_404
from .models import *
from .forms import *
from django.core.urlresolvers import reverse,reverse_lazy
from django.db.models import Q


# Create your views here.

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('home:login')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(status__iexact='PUBLISHED',content_type__iexact='ANNOUNCE')[:10]
        return context

class ProfileView(LoginRequiredMixin, UpdateView):

    form_class = ProfileForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_wapper_class'] = 'col-md-12'
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

class BindEmailView(LoginRequiredMixin, UpdateView):
    pass

class NodeListView(LoginRequiredMixin, ListView):

    template_name = 'user/nodes.html'
    context_object_name = 'nodeLists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['node_tag'] = get_object_or_404(NodeTag, slug= tag_slug)
        return context

    def get_queryset(self):
        queryset = Node.objects.filter(~Q(status__iexact='OUT'))
        tag_slug = self.kwargs.get('tag_slug')
        #print(tag,type(tag))
        if tag_slug:
            queryset = queryset.filter(tags= tag_slug)
        return queryset

class NodeQrInfoView(LoginRequiredMixin, DetailView):

    context_object_name = 'node'
    template_name = 'user/node_qr_info.html'
    http_method_names = ['post']

    def get_object(self, queryset=None):
        node = get_object_or_404(Node, ~Q(status__iexact='OUT'), slug= self.request.POST.get('slug',''))
        node.passwd = self.request.user.passwd
        node.port = self.request.user.port
        return node

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__iexact='PUBLISHED',content_type__iexact='ANNOUNCE')
        return queryset

class PostListView(ListView):
    paginate_by = 10
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__iexact='PUBLISHED',content_type__iexact='ANNOUNCE')
        return queryset
