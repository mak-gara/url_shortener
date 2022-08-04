import qrcode
from pathlib import Path
from qrcode.image.svg import SvgPathImage
from django.utils.crypto import get_random_string

def get_unique_slug_or_existing(obj, length):
    if not obj.slug:
        slug_is_wrong = True
        while slug_is_wrong:
            slug = get_random_string(length)
            if type(obj).objects.filter(slug=slug).exists():
                slug_is_wrong = True
            else:
                return slug
    return obj.slug

def get_escaped_domain(request):
    return request.get_host().replace('.', '\.')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_and_save_qrcode(link, path):
    img = qrcode.make(link, image_factory=SvgPathImage)
    img.save(path)
    