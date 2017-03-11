from django.contrib import admin

# Register your models here.

from .models import *
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(User)
admin.site.register(Node)
admin.site.register(NodeTag)

class InviteCodeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.create_user:
            instance.create_user = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(InviteCode, InviteCodeAdmin)

class PostAdmin(SummernoteModelAdmin):

    def save_model(self, request, obj, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.create_user:
            instance.create_user = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(Post, PostAdmin)

