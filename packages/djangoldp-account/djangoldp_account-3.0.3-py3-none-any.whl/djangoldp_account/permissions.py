from django.conf import settings

from djangoldp.permissions import LDPPermissions
from djangoldp.utils import is_anonymous_user


XMPP_SERVERS = set({'51.15.243.248', '212.47.234.179', '2001:bc8:47b0:2711::1'})

if hasattr(settings, 'XMPP_SERVER_IP'):
    XMPP_SERVERS = XMPP_SERVERS.union(getattr(settings, 'XMPP_SERVER_IP'))

def check_client_ip(request):
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        ip = x_forwarded_for.replace(' ', '').split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    if isinstance(ip, list):
        if any(i in ip for i in XMPP_SERVERS):
            return True
    elif ip in XMPP_SERVERS:
        return True

    return False


class IPOpenPermissions(LDPPermissions):
    def has_permission(self, request, view):
        if check_client_ip(request):
            return True
        return super().has_permission(request, view)

    def get_container_permissions(self, request, view, obj=None):
        '''analyses the Model's set anonymous, authenticated and owner_permissions and returns these'''
        from djangoldp.models import Model
        perms = super().get_container_permissions(request, view, obj)
        if is_anonymous_user(request.user):
            if check_client_ip(request):
                perms = perms.union(set(['view']))
        return perms

    def has_container_permission(self, request, view):
        if check_client_ip(request):
            return True
        return super().has_container_permission(request, view)

    def has_permission(self, request, view):
        """concerned with the permissions to access the _view_"""
        if is_anonymous_user(request.user):
            if not self.has_container_permission(request, view):
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if check_client_ip(request):
            return True
        return super().has_object_permission(request, view, obj)
