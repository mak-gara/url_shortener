from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    # password reset system
    path('accounts/password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('accounts/password/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
    path('accounts/password/reset/send/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('accounts/password/reset/', PasswordResetView.as_view(
        template_name='accounts/reset_password.html'), name='reset_password'),
    
    # aplications
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('', include('shortener.urls', namespace='shortener')),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
