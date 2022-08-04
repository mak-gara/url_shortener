import re
from urllib.parse import urlparse
from django import forms

from .models import Link
from .services import link_already_exists


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('long_link',)

    def __init__(self, user, regex, *args, **kwargs):
        self.user = user
        self.regex = regex
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        long_link = cleaned_data.get('long_link')
        if long_link:
            long_link_path = urlparse(long_link).path[1:]
            if re.match(self.regex, long_link):
                if link_already_exists(long_link_path):
                    raise forms.ValidationError(
                        'An already shortened link cannot be shortened.')
        return cleaned_data

    def save(self):
        form = super().save(commit=False)
        if self.user.is_authenticated:
            form.user = self.user
        form.save()
        return form
