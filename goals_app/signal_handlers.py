from datetime import timedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from celery.result import AsyncResult

from goals_app import models, tasks


@receiver(
    post_save,
    sender=models.Task,
    dispatch_uid='post_save_task_expiration_scheduling'
)
def task_expiration_scheduler(instance, **kwargs):
    finish_date = instance.finish_date + timedelta(days=1)
    tasks.make_task_expired.apply_async(
        (instance.pk,),
        eta=finish_date,
        task_id=str(instance.pk)
    )


@receiver(
    post_delete,
    sender=models.Task,
    dispatch_uid='post_delete_task_expiration_revoker'
)
def task_expiration_revoker(instance, **kwargs):
    task_id = str(instance.pk)
    AsyncResult(task_id).revoke()
