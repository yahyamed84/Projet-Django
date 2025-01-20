from django.contrib.auth import login
from django.contrib.auth.models import User

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Obtenir ou créer un utilisateur par défaut
            user, created = User.objects.get_or_create(
                username='default_admin',
                defaults={
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                user.set_password('default_password')
                user.save()
            login(request, user)
        
        response = self.get_response(request)
        return response
