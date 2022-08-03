from django.urls import path

from .views import HomepageTemplateView, RedirectSomewhereView

app_name = 'shortener'

urlpatterns = [
    path('<slug:slug>/', RedirectSomewhereView.as_view(), name='redirect_somewhere'),
    path('', HomepageTemplateView.as_view(), name='homepage'),
]
    