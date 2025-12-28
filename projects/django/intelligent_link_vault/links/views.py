from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F
from .models import Link

class LinkListView(LoginRequiredMixin, ListView):
    model = Link
    template_name = 'links/link_list.html'
    context_object_name = 'links'
    
    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user).order_by('-created_at')

class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    template_name = 'links/link_form.html'
    fields = ['original_url']
    success_url = reverse_lazy('link-list') 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class LinkRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs.get('short_code')
        link = get_object_or_404(Link, short_code=short_code)
        Link.objects.filter(id=link.id).update(clicks=F('clicks') + 1)
        return link.original_url