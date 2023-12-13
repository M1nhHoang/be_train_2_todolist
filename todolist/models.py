from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_lifecycle import LifecycleModelMixin, hook

# Create your models here.


class Base(LifecycleModelMixin, models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)

    @hook('before_update')
    def onUpdate(self):
        self.update_at = timezone.now()

    class Meta:
        abstract = True


class Task(Base):
    task_name = models.TextField(max_length=250)
    note = models.TextField(max_length=500, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    @hook('before_save')
    def onBeforeSave(self):
        if self.end_date < self.start_date:
            raise ValidationError("Ngày bắt đầu phải nhỏ hơn ngày kết thúc!")

    def __str__(self) -> str:
        return self.task_name
