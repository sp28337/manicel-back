import factory
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.user.models import UserProfile

faker = FakerFactory.create()

EXISTS_GOOGLE_USER_ID = 20
EXISTS_GOOGLE_EMAIL = "tarakanov191094@yandex.ru"


@register(_name="user_profiles")
class UserProfileFactory(factory.Factory):

    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    password = factory.LazyFunction(lambda: faker.password())
    name = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    admin = factory.LazyFunction(lambda: faker.boolean())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
    google_access_token = None
    created_at = factory.LazyFunction(lambda: faker.date_time())
