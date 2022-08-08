from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages

from shortener.models import Link

from .forms import ChangeUserInfoForm, RegisterUserForm
from .models import CustomUser
from .services import signer


class ShortenerLoginView(LoginView):
    template_name = 'accounts/login.html'


class ShortenerProfile(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    context_object_name = 'links'
    paginate_by = 6
    
    def get_queryset(self):
        return Link.get_user_links(self.request)


class ShortenerLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'User data changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ShortenerPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Password changed'


class RegisterUserView(CreateView):
    model = CustomUser
    template_name = 'accounts/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('accounts:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'accounts/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')
    user = get_object_or_404(CustomUser, username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/delete_user.html'
    success_url = reverse_lazy('shortener:homepage')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(CustomUser, pk=self.user_id)
