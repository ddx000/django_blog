from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        """
        https://docs.djangoproject.com/en/3.0/ref/applications/
        Subclasses can override this method to perform initialization tasks such as registering signals.
        It is called as soon as the registry is fully populated.
        Must Import!!! otherwise we don't know who is receiver
        """
        import user.signals
