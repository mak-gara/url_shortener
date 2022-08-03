from django.urls import path

from .views import NewsletterSubscriptionView

app_name = 'mailing'

urlpatterns = [
    path('subscribe/', NewsletterSubscriptionView.as_view(), name='subscribe'),
]