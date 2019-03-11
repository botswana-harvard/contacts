from django.contrib.auth.models import User
from django.db import models


from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber


class Contact(User, BaseUuidModel):

    department = models.CharField(
        verbose_name='Department',
        max_length=250)

    position = models.CharField(
        verbose_name='Position',
        max_length=250)

    cell = EncryptedCharField(
        verbose_name='Cell number',
        validators=[CellNumber, ],
        blank=True,
        null=True,
        help_text='')

    cell_alt = EncryptedCharField(
        verbose_name='Cell (alternate)',
        validators=[CellNumber, ],
        blank=True,
        null=True)

    phone = EncryptedCharField(
        verbose_name='Telephone',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    phone_extension = EncryptedCharField(
        verbose_name='BHP Telephone Extension',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    phone_alt = EncryptedCharField(
        verbose_name='Telephone (alternate)',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    class Meta:
        verbose_name_plural = 'contacts'


    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name}, {self.last_name}'

    def __str__(self):
        return f'{self.full_name}'
