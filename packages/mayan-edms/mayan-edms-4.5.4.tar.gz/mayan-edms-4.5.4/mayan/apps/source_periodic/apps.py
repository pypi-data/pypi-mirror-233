from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .methods import factory_method_periodic_task_save


class SourcePeriodicApp(MayanAppConfig):
    app_namespace = 'source_periodic'
    app_url = 'source_periodic'
    has_tests = True
    name = 'mayan.apps.source_periodic'
    verbose_name = _('Source periodic')

    def ready(self):
        super().ready()

        PeriodicTask = apps.get_model(
            app_label='django_celery_beat', model_name='PeriodicTask'
        )

        PeriodicTask.add_to_class(
            name='save', value=factory_method_periodic_task_save(
                super_save=PeriodicTask.save
            )
        )
