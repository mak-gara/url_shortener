from email import message
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import MailForm

class NewsletterSubscriptionView(View):
    def post(self, request):
        form = MailForm(request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})