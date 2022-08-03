from common.util.utils import get_client_ip
from .models import Link, Transition

def link_already_exists(slug):
    return Link.objects.filter(slug=slug).exists()

def add_transition(request, obj):
    Transition.objects.create(link=obj, ip=get_client_ip(request))
    