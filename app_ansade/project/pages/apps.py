from django.apps import AppConfig

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Gestion des Pages'  # Nom lisible dans l'administration
