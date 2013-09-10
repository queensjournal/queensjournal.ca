import factory
from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = 'tball'
    first_name = 'Tyler'
    last_name = 'Ball'
    email = 'tyler@tylerball.net'
