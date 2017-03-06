# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from . import utils
import random, base64
from django.core import validators
from django.urls import reverse
from django_summernote.models import AbstractAttachment

def get_usefull_port():
    max_port = User.objects.aggregate(Max('port')).get('port__max', 13215)
    new_port = int(max_port) + random.randint(2, 5)
    return new_port

# 用户模型.
class User(AbstractUser):

    avatar = models.CharField(verbose_name='头像', max_length=63,default='avatar1.png')
    port = models.PositiveSmallIntegerField(verbose_name='端口',unique=True, default= get_usefull_port)
    passwd = models.CharField(verbose_name='端口密码',max_length=16,default=utils.gen_passwd)
    t = models.IntegerField(verbose_name='最后使用时间戳',default=0)
    u = models.BigIntegerField(verbose_name='上传流量',default=0)
    d = models.BigIntegerField(verbose_name='下载流量',default=0)
    transfer_enable = models.BigIntegerField(verbose_name='每月流量限额',default=0)
    switch = models.BooleanField(verbose_name='流量开关状态',default=True)
    last_check_in_time = models.DateTimeField(verbose_name='最后签到时间',null=True)
    check_in_count = models.IntegerField(verbose_name='连续签到次数',default=0)

    reg_ip = models.GenericIPAddressField(verbose_name='注册IP',unpack_ipv4=True,null=True)
    last_login_ip = models.GenericIPAddressField(verbose_name='上次登录IP',unpack_ipv4=True,null=True)
    last_login_date = models.DateTimeField(verbose_name='上次登录时间',null=True,auto_now_add=True)
    this_login_ip = models.GenericIPAddressField(verbose_name='本次登录IP',unpack_ipv4=True,null=True)
    this_login_date = models.DateTimeField(verbose_name='本次登录时间',null=True,auto_now_add=True)

    invite_num = models.IntegerField(verbose_name='可以生成邀请码的个数',default=0)
    last_gen_invite_code_time = models.DateTimeField(verbose_name='上次生成邀请码时间',null=True)

    email_validate_code = models.CharField(max_length=63,verbose_name='邮箱验证码',default=utils.gen_val_code)
    bind_email = models.PositiveSmallIntegerField(verbose_name='是否已验证邮箱',choices=((1,'已验证'),(0,'未验证')),default=0)

    wx_validate_code = models.CharField(max_length=31,verbose_name='微信公众号验证码',default=utils.gen_val_code)
    wxopenid = models.CharField(max_length=127,verbose_name='微信OPENID',null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

#节点模型
class Node(models.Model):
    METHOD_CHOICES = (
        ('rc4-md5', 'rc4-md5'),
        ('chacha20', 'chacha20'),
        ('aes-256-cfb', 'aes-256-cfb'),
        ('aes-192-cfb', 'aes-192-cfb'),
        ('aes-128-cfb', 'aes-128-cfb'),
        ('salsa20', 'salsa20'),
        ('rc4', 'rc4'),
        ('table', 'table'),
    )

    STATUS_CHOICES = (
        ('ON-LINE','正常'),
        ('OFF-LINE','离线'),
        ('BANDWIDTH-OVER','流量用完'),
        ('ATTACKED','被攻击中'),
        ('INIT','初始化中'),
        ('MAINTAIN','维护中'),
        ('OUT','下线'),
    )
    id = models.CharField(max_length=63, verbose_name='主键、API Key', primary_key=True, default=utils.gen_api_key, editable=False)
    name = models.CharField(max_length=63,verbose_name='节点名称')
    location = models.CharField(max_length=127, verbose_name='节点位置')
    ip = models.GenericIPAddressField(verbose_name='节点IP地址',protocol='IPv4')
    ipv6 = models.GenericIPAddressField(blank=True, null= True , protocol='IPv6', verbose_name='节点IPv6地址')
    method = models.CharField(choices=METHOD_CHOICES,max_length=63, default='chacha20', verbose_name='节点加密方式')
    info = models.TextField(max_length=255, verbose_name='节点信息')
    status = models.CharField(max_length=63, choices=STATUS_CHOICES,default='INIT', verbose_name='节点状态')
    traffic_rate = models.DecimalField(verbose_name='流量倍率', max_digits=8, decimal_places=2, default=1.00)
    sort = models.SmallIntegerField(verbose_name='排序', default=0, help_text='小的在前面')
    tags = models.ManyToManyField('NodeTag', verbose_name='标签集合', blank=True)

    #SSR属性
    ORIGIN_CHOICES = (
        ('origin','origin：原版协议'),
        ('auth_sha1_v4','auth_sha1_v4：较高安全性，有宽松的时间校对要求，混淆强度大'),
        ('auth_aes128_md5','auth_aes128_md5：最高安全性，有宽松的时间校对要求，计算量相对高一些，混淆强度较大'),
        ('auth_aes128_sha1','auth_aes128_sha1：最高安全性，有宽松的时间校对要求，计算量相对高一些，混淆强度较大'),
        ('auth_sha1_v4_compatible','auth_sha1_v4_compatible，兼容版'),
    )
    protocol = models.CharField(max_length=63,verbose_name='协议插件',default='auth_sha1_v4_compatible',choices=ORIGIN_CHOICES,help_text='协议推荐：协议用auth_aes128_md5或auth_aes128_sha1最佳（但是不支持原版SS协议），此时即使使用rc4加密亦可，混淆随意；_compatible后缀表示兼容原版SS协议')
    protocol_param = models.CharField(max_length=63,verbose_name='协议插件参数',blank=True,default='')
    OBFS_CHOICES = (
        ('plain','plain：不混淆，无参数'),
        ('tls1.2_ticket_auth','tls1.2_ticket_auth：伪装为tls请求。参数配置与http_simple一样'),
        ('http_simple','http_simple：简易伪装为http get请求'),
        ('http_post','http_post：与http_simple绝大部分相同，POST伪装方式'),
        ('tls1.2_ticket_auth_compatible','tls1.2_ticket_auth_compatible：兼容版'),
        ('http_simple_compatible','http_simple_compatible：兼容版'),
        ('http_post_compatible','http_post_compatible：兼容版'),
    )
    obfs = models.CharField(max_length=127,verbose_name='混淆插件',choices=OBFS_CHOICES,default='tls1.2_ticket_auth_compatible',
                            help_text='混淆推荐：如果QoS在你的地区明显，混淆建议在http_simple与tls1.2_ticket_auth中选择，具体选择可以通过自己的试验得出。如果选择混淆后反而变慢，那么混淆请选择plain。如果你不在乎QoS，但担心你的个人vps能不能持久使用，那么混淆选择plain或tls1.2_ticket_auth，协议选择auth_aes128_md5或auth_aes128_sha1')
    obfs_param = models.CharField(max_length=63,verbose_name='混淆插件参数',blank=True,default='')

    ssh_port = models.PositiveSmallIntegerField(verbose_name='SSH端口号',default=22)

    #api_key = models.CharField(verbose_name='API Key',unique=True,max_length=127,default=utils.gen_api_key, editable=False)
    api_secret = models.CharField(max_length=255,verbose_name='API Secret 密匙',default=utils.gen_api_secret)

    class Meta:
        verbose_name = '节点'
        verbose_name_plural = verbose_name
        ordering = ['sort','id']

    def __str__(self):
        return '%s[%s]'%(self.name,self.ip)


    passwd = ''
    port = ''

    @property
    def ss_url(self):
        return 'ss://%s' % (self.ss_protocol,)

    @property
    def ss_qrcode(self):
        return 'ss://%s' % (base64.encodebytes(self.ss_protocol.encode()).decode().strip(),)

    @property
    def ss_protocol(self):
        return '%s:%s@%s:%s' % (self.method, self.passwd, self.ip, self.port)

#节点标签模型
class NodeTag(models.Model):

    slug = models.CharField(max_length=63,verbose_name='标识', help_text='请使用字母、数字、下划线、中划线组成，不可重复', primary_key=True,
                validators= (validators.RegexValidator(r'[\w-]+'),), unique=True,)
    name = models.CharField(max_length=63, verbose_name='标签名称')

    class Meta:
        verbose_name = '节点标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s:%s' % (self.slug, self.name)

#邀请码模型
class InviteCode(models.Model):

    code = models.CharField(max_length=127,verbose_name='邀请码',default=utils.gen_invite_code,unique=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    used_time = models.DateTimeField(null=True,verbose_name='使用时间')
    TYPE_DEFAULT = 'DEFAULT'
    TYPE_TIMING = 'TIMING'
    TYPE_USERS = 'USERS'
    TCHOICES = (
        (TYPE_DEFAULT,'默认类型'),
        (TYPE_TIMING,'定时发放类型'),
        (TYPE_USERS,'用户生成类型'),
    )
    type = models.CharField(max_length=15,verbose_name='邀请码类型',default=TYPE_DEFAULT,choices=TCHOICES)
    show_time = models.DateTimeField(null=True,verbose_name='公开显示时间')

    create_user = models.ForeignKey(User,null=True,verbose_name='创建者',on_delete=models.SET_NULL,related_name='created_code_set')
    used_user = models.ForeignKey(User,null=True,verbose_name='使用者',on_delete=models.SET_NULL,related_name='used_code_set')

    traffic = models.BigIntegerField(verbose_name='流量',default=0)
    enable = models.BooleanField(verbose_name='是否可用',default=True)

    class Meta:
        verbose_name = '邀请码'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return '[%s]%s'%(self.code,'可用' if self.enable else '失效')

#站内文章模型
class Post(models.Model):
    slug = models.CharField(max_length=255,verbose_name='内容标识Slug', unique=True,
                validators= (validators.RegexValidator(r'[\w-]+'),),
                help_text='请使用字母、数字、下划线、中划线组成，不可重复')
    title = models.CharField('标题', max_length=255)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间',auto_now=True)
    status = models.CharField('文章状态', max_length=31, choices=(('PUBLISHED','已发布'),('DRAFT','草稿')), default='DRAFT')
    content_type = models.CharField('内容类型', max_length=31, choices=(('ANNOUNCE', '站内通告'), ('PAGE','页面'), ('OTHER', '其他类型')), default= 'ANNOUNCE')
    abstract = models.CharField('摘要', max_length=63, blank=True, null=True, help_text="可选，如若为空将摘取正文的前54个字符")
    topped = models.BooleanField('置顶', default=False)

    def __str__(self):
        return '%s [%s]'%(self.title, self.get_status_display())

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name
        ordering = ['-topped','-last_modified_time']

    def get_absolute_url(self):
        return reverse('user:post_detail', kwargs={'pk': self.pk})


#附件模型
class Attachment(AbstractAttachment):
    rename = models.BooleanField(verbose_name='是否重命名', default=True,
        help_text='如果选中，则会随机重命名；否则不会重命名，但是有覆盖已有同名文件风险。')

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = verbose_name
        ordering = ['-uploaded']
