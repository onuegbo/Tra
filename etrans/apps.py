from django.apps import AppConfig


class EtransConfig(AppConfig):
    name = 'etrans'

    def ready(self):
        import etrans.signals.handlers




