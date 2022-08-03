from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView, RedirectView

from common.util.utils import get_escaped_domain
from .services import add_transition

from .forms import LinkForm
from .models import Link


class HomepageTemplateView(View):
    def get(self, request):
        return render(request, 'shortener/index.html')

    def post(self, request):
        regex = f'^{request.scheme}:\/\/{get_escaped_domain(request)}\/[a-zA-Z0-9]' + '{7}$'
        form = LinkForm(request.user, regex, request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'short_link': f'{request.scheme}://{request.get_host()}/{obj.slug}',
                                 'long_link': obj.long_link})
        return JsonResponse({'short_link': None})


class RedirectSomewhereView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Link, slug=self.kwargs['slug'])
        add_transition(self.request, obj)
        return obj.long_link
