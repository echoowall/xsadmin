from django.shortcuts import render, render_to_response
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout,update_session_auth_hash
from django.shortcuts import redirect,get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import *
from .forms import *
from django.core.urlresolvers import reverse,reverse_lazy
from django.db.models import Q, F, Sum, fields
from django.http import HttpResponseRedirect

from home.views import GeeCaptchaValidateMixin
from django.utils import timezone
from datetime import datetime, timedelta
from home import utils as home_utils
from django.db import transaction
from django.http import JsonResponse


TO_MB = 1048576
TO_GB = 1073741824

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
        trans_list = TrafficRecord.objects.filter(port=self.request.user.port,type=1,summary_date__gt=timezone.now()-timedelta(31)).\
                    values('summary_date').annotate(sum_u=Sum(F('u')*F('rate')/100, output_field=fields.IntegerField()),
                    sum_d=Sum(F('d')*F('rate')/100, output_field=fields.IntegerField())).order_by('summary_date')
        #print(trans_list)
        trans_date = list()
        trans_u = list()
        trans_d = list()
        for tran in trans_list:
            trans_date.append(tran['summary_date'].strftime('%Y-%m-%d'))
            trans_u.append(round(tran['sum_u']/TO_MB, 2))
            trans_d.append(round(tran['sum_d']/TO_MB, 2))
        context['trans_date'] = trans_date
        context['trans_u'] = trans_u
        context['trans_d'] = trans_d
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

class PersonalProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/personal_profile.html'


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

class CheckInView(LoginRequiredMixin, GeeCaptchaValidateMixin, TemplateView):
    template_name = 'user/checkin.html'
    success_url = reverse_lazy('user:checkin')
    unable_checkin_reason = None

    def check_user_checkable(self, user):
        if not user.is_active or user.switch == 0:
            self.unable_checkin_reason = '用户被禁用，暂时无法签到'
            return False
        last_check_in_time = user.last_check_in_time
        if last_check_in_time:
            now = timezone.now()
            return last_check_in_time < now and now.strftime('%Y-%m-%d') != last_check_in_time.strftime('%Y-%m-%d')
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_checkable'] = self.check_user_checkable(self.request.user)
        context['unable_checkin_reason'] = self.unable_checkin_reason
        context['check_in_list'] = ActionRecord.objects.filter(create_user=self.request.user,
                                                               type='USER_CHECK_IN').order_by('-id')[:7]
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        if self.check_user_checkable(user):
            #进入签到逻辑
            now = timezone.now()
            yesterday_morning = timezone.make_aware(datetime(now.year, now.month, now.day-1))
            if not user.last_check_in_time or user.last_check_in_time < yesterday_morning:
                count = 1
            else:
                count = user.check_in_count + 1
            trans_gift = random.randint(10, 120)
            user.check_in_count = count
            user.last_check_in_time = now
            user.transfer_enable = F('transfer_enable')+TO_MB*trans_gift
            #赠送适当流量
            user.save()
            ActionRecord(type='USER_CHECK_IN', remark='您已连续签到%d天，获赠%dM流量'%(count,trans_gift), meta="{'count':'%d'}" % count,
                         create_user=user, ip=home_utils.get_remote_ip(request)).save()
        return HttpResponseRedirect(self.success_url)


class BindEmailView(LoginRequiredMixin, UpdateView):
    pass

class SwitchNodeGroupView(LoginRequiredMixin, GeeCaptchaValidateMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        now = timezone.now()
        if not user.last_change_node_group_time or user.last_change_node_group_time + timedelta(hours=72) < now:
            node_group_id = request.POST.get('node_group_id')
            if node_group_id:
                user.last_change_node_group_time = timezone.now()
                user.node_group_id = node_group_id
                user.save()
        return HttpResponseRedirect(reverse('user:nodes'))

class NodeListView(LoginRequiredMixin, ListView):

    template_name = 'user/nodes.html'
    context_object_name = 'nodeLists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lastchange = self.request.user.last_change_node_group_time
        if lastchange:
            switchable_time = lastchange + timedelta(hours=72)
            node_group_switchable = True if switchable_time<timezone.now() else False
        else:
            switchable_time = timezone.now()
            node_group_switchable = True
        context['node_group_switchable_time'] = switchable_time
        context['node_group_switchable'] = node_group_switchable
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['node_tag'] = get_object_or_404(NodeTag, slug= tag_slug)
        else:
            context['node_tag'] = None
        return context

    def get_queryset(self):
        queryset = Node.objects.filter(~Q(status__iexact='OUT')&Q(node_group_id=self.request.user.node_group_id))
        tag_slug = self.kwargs.get('tag_slug')
        #print(tag,type(tag))
        if tag_slug:
            queryset = queryset.filter(tags= tag_slug)
        return queryset

class DownloadNodeCfgView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        queryset = Node.objects.filter(~Q(status__iexact='OUT')&Q(node_group_id=self.request.user.node_group_id))
        servers = list()
        user = request.user
        for s in queryset:
            server = dict()
            server['server'] = s.ip
            server['server_port'] = user.port
            server['password'] = user.passwd
            server['method'] = s.method
            server['remarks'] = s.name
            server["protocol"] = s.protocol
            server["protocolparam"] = s.protocol_param
            server["obfs"] = s.obfs
            server["obfsparam"] = s.obfs_param
            servers.append(server)

        cfg = {"configs": servers,
               "index": 0,"global":False,"enabled":True,
               "shareOverLan":False,"isDefault":False,
               "localPort":1080,"pacUrl":None,"useOnlinePac":False}
        response = JsonResponse(cfg)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=gui-config.json'
        return response


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


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__iexact='PUBLISHED',content_type__iexact='ANNOUNCE')
        return queryset

class PostListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset().filter(status__iexact='PUBLISHED',content_type__iexact='ANNOUNCE')
        return queryset


def node_api_info_viem(request, object_id, model_admin):
    admin_site = model_admin.admin_site
    opts = model_admin.model._meta
    node = get_object_or_404(Node, pk=object_id)
    context = {
        'admin_site': admin_site.name,
        'opts': opts,
        'title': '节点API信息',
        'cl':model_admin.model._meta,
        'current_site': get_current_site(request),
        #'root_path': '%s' % admin_site.root_path,
        'secure': request.is_secure(),
        'app_label': opts.app_label,
        'node': node,
    }
    return render_to_response('user/node_admin_api_info.html', context)