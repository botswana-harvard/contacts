from django.db import models

from edc_base.model_mixins import BaseUuidModel

class Department(BaseUuidModel):

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
