from django.contrib import admin

# Register your models here.

from .models import *
from .forms import *
from django_summernote.admin import SummernoteModelAdmin
from django.conf.urls import url

def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = '禁用用户'
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = '启用用户'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined','is_staff', 'is_active')
    search_fields = ('username','email')
    list_filter = ('is_active','is_staff')
    actions = [make_inactive,make_active]

admin.site.register(User, UserAdmin)

class NodeAdmin(admin.ModelAdmin):
    change_form_template = 'user/node_admin_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r'^node_api_info/(?P<id>\d+)/$',self.admin_site.admin_view(self.node_api_info_viem), name='node_api_info')]
        return my_urls + urls

    def node_api_info_viem(self, reqeust, id):
        from .views import node_api_info_viem
        return node_api_info_viem(reqeust,id,self)

    list_display = ('name', 'location', 'ip','method','traffic_rate','status', 'sort')
    search_fields = ('name','location','info','remark_for_admin')
    list_filter = ('status',)
    fieldsets = (
        (None, {'fields': ('name','ip','location','method','status','traffic_rate','info')}),
        ('更多信息', {'classes': ('collapse',),
        'fields': ('ipv6','sort','remark_for_admin','tags','protocol','protocol_param',
                   'obfs','obfs_param','ssh_port')}),
    )

admin.site.register(Node,NodeAdmin)
admin.site.register(NodeTag)


class InviteCodeAdmin(admin.ModelAdmin):
    form = InviteCodeForm
    list_display = ('code','type','create_time','enable')
    search_fields = ('code',)
    list_filter = ('enable',)
    fieldsets = (
        (None,{'fields':('count',)}),
        ('更多信息', {'classes': ('collapse',),'fields': ('type','show_time','traffic')}),
    )
    def save_model(self, request, obj, form, change):
        count = form.cleaned_data['count']
        #提交的有用的数据：
        type = form.cleaned_data['type']
        show_time = form.cleaned_data['show_time']
        traffic = form.cleaned_data['traffic']
        for n in range(count):
            code = InviteCode(type=type,show_time=show_time,traffic=traffic,create_user=request.user)
            code.save()
        return code

admin.site.register(InviteCode, InviteCodeAdmin)

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'content_type', 'last_modified_time', 'status')
    search_fields = ('title',)
    list_filter = ('status','content_type')
    def save_model(self, request, obj, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.create_user:
            instance.create_user = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(Post, PostAdmin)

