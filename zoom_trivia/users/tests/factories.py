from django.contrib.auth import get_user_model
import factory

class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    name = factory.Faker("name")
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
