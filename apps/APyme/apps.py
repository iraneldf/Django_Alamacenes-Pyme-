from django.apps import AppConfig


class ApymeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.APyme'
    verbose_name = 'Almacenes Pyme'

    # add this
    def ready(self):
        from apps.APyme.jobs import updater
        updater.start()
        import apps.APyme.signals  # noqa
