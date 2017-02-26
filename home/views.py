from django.shortcuts import render
from django.views.generic import *
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
    template_name = 'home/about.html'
