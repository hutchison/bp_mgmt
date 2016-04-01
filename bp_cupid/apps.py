from django.apps import AppConfig, apps
from actstream import registry

class BPCupidConfig(AppConfig):
    name = 'bp_cupid'
    verbose_name = 'BP Cupid'

    def ready(self):
        registry.register(apps.get_model('auth.user'))
        registry.register(apps.get_model('bp_cupid.Student'))
        from bp_cupid import signals
