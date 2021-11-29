import pytest

from datetime import datetime

from faker import Faker

from goals_app import models

fake = Faker()


def clean_kwargs(defaults, **kwargs):
    """
    Replace missing keyword arguments with provided defaults.

    :param defaults: Dict containing default values and formatted as follows:
    {
        "kwarg": {
                    "value": value or callable,
                    "args": (True,), positional args to pass to the callable
                    "kwargs": {"a": 5} keyword args to pass to the callable
        }
    }
    :param kwargs: kwargs to clean.
    :return: kwargs with missing values replaced with provided defaults.
    """
    for kwarg, default_data in defaults.items():
        should_not_pass = kwarg + '__empty' in kwargs
        if kwarg not in kwargs and not should_not_pass:
            default_value = default_data['value']
            if callable(default_value):
                call_args = default_data.get('args', ())
                call_kwargs = default_data.get('kwargs', {})
                default_value = default_value(*call_args, **call_kwargs)
            kwargs[kwarg] = default_value

    return {k: v for k, v in kwargs.items() if '__empty' not in k}


def create_user(**kwargs):
    """
    Creates new user with auto generated fields values if explicit ones were
    not provided.
    :param kwargs: Keyword arguments to pass to User.object.create.
    :return: User instance.
    """
    defaults = {
        'username': {'value': fake.user_name},
        'email': {'value': fake.email},
        'password': {'value': fake.password, 'args': (16,)},
        'first_name': {'value': fake.first_name},
        'last_name': {'value': fake.last_name}
    }

    kwargs = clean_kwargs(defaults, **kwargs)

    return models.User.objects.create_user(**kwargs)


def create_category(**kwargs):
    """
    Creates new category with auto generated fields values if explicit ones were
    not provided.
    :param kwargs: Keyword arguments to pass to Category.object.create.
    :return: Category instance.
    """
    defaults = {
        'name': {'value': fake.sentence, 'args': (2, )}
    }

    kwargs = clean_kwargs(defaults, **kwargs)

    return models.Category.objects.create(**kwargs)


def create_task(**kwargs):
    """
    Creates new task with auto generated fields values if explicit ones were
    not provided.
    Default user is created with create_user.
    Default category is created with create_category.
    :param kwargs: Keyword arguments to pass to Task.object.create.
    :return: Task instance.
    """
    # Save start_date to make sure that default finish_date is greater.
    start_date = kwargs.get('start_date', None)
    if start_date:
        # Workaround
        # faker.date_between doesn't support date string
        # https://github.com/joke2k/faker/issues/1571
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = kwargs.get('start_date', fake.date_object('+100y'))

    defaults = {
        'todo': {'value': fake.sentence},
        'creator': {'value': create_user},
        'start_date': {'value': start_date},
        'finish_date': {'value': fake.date_between, 'args': (
            start_date,
            '+100y'
        )},
        'reason': {'value': fake.sentence},
        'category': {'value': create_category}
    }

    kwargs = clean_kwargs(defaults, **kwargs)

    return models.Task.objects.create(**kwargs)


class Instance:
    """
    Provides instance created with given method.
    Handles creation and destruction of the instance.
    """
    def __init__(self, create, name):
        """
        :param create: Function to create model instance.
        :param name: Name of the class property to assign instance to.
        """
        self.name = name
        self._create = create

    def class_fixture(self, django_db_blocker, request):
        """
        Assigns model instance created with self._create to class attribute
        with name equal to self.name.

        Should be used as fixture with 'class' scope.
        :param django_db_blocker: Fixture to enable DB access.
        :param request: Fixture that provide information on the executing
        test function.
        :return: None
        """
        instance = self._fixture(django_db_blocker, request)
        setattr(request.cls, self.name, instance)

    def function_fixture(self, django_db_blocker, request):
        """
        Returns model instance created with self._create.

        Should be used as fixture with 'function' scope.
        :param django_db_blocker: Fixture to enable DB access.
        :param request: Fixture that provide information on the executing
        test function.
        :return: Model instance.
        """
        return self._fixture(django_db_blocker, request)

    def _fixture(self, django_db_blocker, request):
        """
        Internal implementation of fixture used by concrete methods.
        :param django_db_blocker:
        :param request: Fixture that provide information on the executing
        test function.
        :return: Model instance.
        """
        with django_db_blocker.unblock():
            instance = self._create()

        def destroy():
            with django_db_blocker.unblock():
                return self._destroy(instance)

        request.addfinalizer(destroy)
        return instance

    def _destroy(self, instance):
        """
        Handles destruction of created instance.
        :param instance: Model instance.
        :return: Return value of Django's Model.delete.
        """
        if instance.pk:
            return instance.delete()


class AutomatedFactory:
    """
    Provides factory method that handles creation and destruction of instances.
    Before using fixtures should be wrapped
    """
    def __init__(self, create, name=None):
        """
        :param create: Function to create model instances.
        :param name: Name of the factory. Provides factory to test class under
        this name as class method name.
        """
        self._create = create
        self.cls_attr_name = name or create.__name__
        self.instances = []

    def class_fixture(self, django_db_blocker, request):
        """
        Assigns factory function to class attribute with name equal to
        self.name.

        Should be used as fixture with 'class' scope.
        :param django_db_blocker: Fixture to enable DB access.
        :param request: Fixture that provide information on the executing
        test function.
        :return: None
        """
        instance = self._fixture(django_db_blocker, request)
        setattr(request.cls, self.cls_attr_name, instance)

    def function_fixture(self, django_db_blocker, request):
        """
        Returns factory function.

        Should be used as fixture with 'function' scope.
        :param django_db_blocker: Fixture to enable DB access.
        :param request: Fixture that provide information on the executing
        test function.
        :return: Factory function.
        """
        return self._fixture(django_db_blocker, request)

    def _fixture(self, django_db_blocker, request):
        """
        Internal implementation of fixture used by concrete methods.
        :param django_db_blocker: Fixture to enable DB access.
        :param request: Fixture that provide information on the executing
        test function.
        :return: Factory function.
        """
        factory = self._factory(django_db_blocker)

        def destroy():
            """
            Handles destruction of model instances created with factory function.
            :return: Return value of Django's Model.delete.
            """
            with django_db_blocker.unblock():
                return self._destroy()

        request.addfinalizer(destroy)
        return factory

    def _factory(self, django_db_blocker):
        """
        Wraps self._create into db_access_wrapper and returns it.
        :param django_db_blocker: Fixture to enable DB access.
        :return: Wrapped self._create function.
        """

        @staticmethod
        def db_access_wrapper(*args, **kwargs):
            """
            Wraps self._create to provide it access to DB.
            :param args: Positional arguments to pass to self._create.
            :param kwargs: Keyword arguments to pass to self._create.
            :return:
            """
            with django_db_blocker.unblock():
                instance = self._create(*args, **kwargs)
                self.instances.append(instance)
                return instance

        return db_access_wrapper

    def _destroy(self):
        """
        Deletes created model instances.
        :return: Return value of Django's Model.delete.
        """
        for instance in self.instances:
            if instance.pk:
                return instance.delete()


UserFactory = AutomatedFactory(create_user, 'user_factory')
user_factory_class_fixture = pytest.fixture(
    scope='class'
)(UserFactory.class_fixture)

UserInstance = Instance(create_user, 'user')
user_instance_class_fixture = pytest.fixture(
    scope='class'
)(UserInstance.class_fixture)

TaskFactory = AutomatedFactory(create_task, 'task_factory')
task_factory_class_fixture = pytest.fixture(
    scope='class'
)(TaskFactory.class_fixture)

TaskInstance = Instance(create_task, 'task')
task_instance_class_fixture = pytest.fixture(
    scope='class'
)(TaskInstance.class_fixture)

CategoryFactory = AutomatedFactory(create_category, 'category_factory')
category_factory_class_fixture = pytest.fixture(
    scope='class'
)(CategoryFactory.class_fixture)

CategoryInstance = Instance(create_category, 'category')
category_instance_class_fixture = pytest.fixture(
    scope='class'
)(CategoryInstance.class_fixture)
