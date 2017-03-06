from django.contrib import admin

# Register your models here.

from .models import *
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(User)
admin.site.register(Node)
admin.site.register(NodeTag)
admin.site.register(InviteCode)

class PostAdmin(SummernoteModelAdmin):
    pass

admin.site.register(Post, PostAdmin)

