from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.models import Group
from apps.galeria.models import UrlPermission

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir superusuários sem verificação de permissões
        if request.user.is_superuser:
            return self.get_response(request)
        
        url_name = resolve(request.path_info).url_name
        if url_name:
            try:
                url_permission = UrlPermission.objects.get(url=url_name)
                required_permission = url_permission.permissions.first().codename

                print(f"URL name: {url_name}")
                print(f"Required permission: {required_permission}")
                
                # Obter permissões do usuário e do grupo
                user_permissions = set(request.user.user_permissions.values_list('codename', flat=True))
                group_permissions = set()
                for group in request.user.groups.all():
                    group_permissions.update(group.permissions.values_list('codename', flat=True))
                
                all_permissions = user_permissions.union(group_permissions)
                print(f"User permissions: {user_permissions}")
                print(f"Group permissions: {group_permissions}")
                print(f"All permissions: {all_permissions}")

                if required_permission in all_permissions:
                    print("User has required permission. Granting access.")
                    return self.get_response(request)  
                else:
                    print("User does not have required permission. Redirecting to login.")
                    return redirect('galeria:acesso_negado')

            except UrlPermission.DoesNotExist:
                print(f"No permissions associated with URL: {url_name}")
                return self.get_response(request) 

        response = self.get_response(request)
        return response
