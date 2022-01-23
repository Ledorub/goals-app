import pytest
import time

from datetime import date

from django.conf import settings
from django.core import exceptions

from goals_app import models
from goals_app.backends import decode_access_token

# Redis server should be running.
# Otherwise pytest will hang silently.


@pytest.mark.usefixtures(
    'user_factory_class_fixture',
    'user_instance_class_fixture'
)
class TestUserModel:
    def test_user_created(self):
        assert self.user_factory()

    def test_raise_on_short_password(self):
        min_pass_len = settings.MIN_PASSWORD_LENGTH
        with pytest.raises(exceptions.ValidationError,
                           match=rf'{min_pass_len}'):
            self.user_factory(password='$h0rt!pa$$')

    def test_raise_on_setting_short_password(self):
        min_pass_len = settings.MIN_PASSWORD_LENGTH

        with pytest.raises(exceptions.ValidationError,
                           match=rf'{min_pass_len}'):
            self.user.set_password('$h0rt!pa$$')

    def test_raise_on_empty_username(self):
        with pytest.raises(ValueError):
            self.user_factory(username='')

    def test_raise_on_empty_email(self):
        with pytest.raises(exceptions.ValidationError):
            self.user_factory(email='')

    def test_no_raise_on_empty_first_name(self):
        assert self.user_factory(first_name='')

    def test_no_raise_on_empty_last_name(self):
        assert self.user_factory(last_name='')

    def test_get_by_natural_key_email(self, db):
        email = self.user.email
        models.User.objects.get_by_natural_key(email)

    def test_new_access_token_on_every_call(self, db):
        assert self.user.generate_access_token() != self.user.generate_access_token()

    def test_new_refresh_token_on_every_call(self, db):
        assert self.user.generate_refresh_token() != self.user.generate_refresh_token()

    def test_generate_token_returns_access_refresh_csrf_tokens(self, db):
        token_names = ['access_token', 'refresh_token', 'csrf_token']
        tokens = self.user.generate_tokens()
        assert all(token_name in tokens for token_name in token_names)

    def test_access_token_contains_csrf_token(self, db):
        tokens = self.user.generate_tokens()
        access_token_payload = decode_access_token(tokens['access_token'])
        assert tokens['csrf_token'] == access_token_payload['csrf']


@pytest.mark.usefixtures(
    'task_factory_class_fixture',
    'task_instance_class_fixture'
)
class TestTaskModel:
    def test_task_created(self):
        assert self.task_factory()

    # def test_raise_on_start_date_in_the_past(self):
    #     with pytest.raises(exceptions.ValidationError):
    #         self.task_factory(start_date='2020-07-14')

    def test_no_raise_on_start_date_in_the_future(self):
        assert self.task_factory(start_date='2030-06-18')

    def test_default_start_date_equals_today(self):
        task = self.task_factory(start_date__empty=None,
                                 finish_date='2023-04-11')
        assert task.start_date == date.today()

    def test_raise_on_finish_date_lt_start_date(self):
        with pytest.raises(exceptions.ValidationError):
            self.task_factory(start_date='2005-03-19', finish_date='2003-08-15')

    def test_default_is_achieved_is_false(self):
        assert not self.task.is_achieved

    def test_raise_on_empty_category(self):
        with pytest.raises(exceptions.ValidationError):
            self.task_factory(category__empty=None)

    def test_category_created_if_doesnt_exist(self, db):
        category_name = 'Cat'
        assert not models.Category.objects.filter(name=category_name)
        self.task_factory(category=category_name)
        models.Category.objects.filter(name=category_name)

    def test_category_used_if_exists(self, db):
        category_name = 'Cat'
        category = models.Category.objects.create(name=category_name)
        task = self.task_factory(category=category_name)
        assert task.category == category

    def test_no_raise_on_empty_parent(self):
        assert self.task_factory(parent__empty=None)

    def test_subtasks_accessible_via_subtasks_field(self, db):
        parent_task = self.task_factory()
        subtask_1 = self.task_factory(parent=parent_task)
        subtask_2 = self.task_factory(parent=parent_task)

        assert parent_task.subtasks
        subtasks = parent_task.subtasks.all()
        assert subtask_1 in subtasks and subtask_2 in subtasks

    def test_raise_on_depth_level_exceeding_2(self):
        l0_task = self.task_factory()
        l1_task = self.task_factory(parent=l0_task)
        l2_task = self.task_factory(parent=l1_task)

        with pytest.raises(RecursionError):
            self.task_factory(parent=l2_task)


@pytest.mark.usefixtures(
    'category_factory_class_fixture',
    'category_instance_class_fixture',
    'task_factory_class_fixture'
)
class TestCategoryModel:
    def test_get_by_natural_key_name(self, db):
        name = self.category.name
        models.Category.objects.get_by_natural_key(name)

    def test_name_capitalized(self):
        name = 'lower case name'
        category = self.category_factory(name=name)
        assert name.capitalize() == category.name

    def test_goals_accessible_via_goals_field(self, db):
        task = self.task_factory(category=self.category.name)
        assert self.category.tasks
        assert task in self.category.tasks.all()
