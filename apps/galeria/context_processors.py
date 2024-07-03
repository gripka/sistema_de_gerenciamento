# galeria/context_processors.py
from django.contrib.auth.decorators import login_required
from .models import UrlPermission

def user_permissions(request):
    user_perms = set()
    if request.user.is_authenticated:
        user_perms = set(request.user.get_all_permissions())
        
    url_permissions = {}
    url_perms = UrlPermission.objects.prefetch_related('permissions').all()
    for url_perm in url_perms:
        url_permissions[url_perm.url] = {perm.codename for perm in url_perm.permissions.all()}
    
    return {
        'user_permissions': user_perms,
        'url_permissions': url_permissions,
    }
