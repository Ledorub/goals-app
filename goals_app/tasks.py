from datetime import date, timedelta

from goals_project import celery_app as app
from goals_app import models


@app.task
def make_task_expired(pk):
    task = models.Task.objects.get(pk=pk)
    if date.today() < task.finish_date + timedelta(days=1):
        return
    task.is_expired = True
    task.save()
