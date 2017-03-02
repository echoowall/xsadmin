from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


# Create your views here.

def logout(request):
    auth_logout(request)
    return redirect('home:login')

class BaseUserView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseUserView, self).get_context_data(**kwargs)
        #context['']
        return context

class DashboardView(BaseUserView):
    template_name = 'user/dashboard.html'


