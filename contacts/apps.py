from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style

from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'contacts'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BHP Directory'
    institution = 'Botswana-Harvard AIDS Institute'
