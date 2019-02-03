from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import PROTECT


from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber


class Contact(BaseUuidModel):


    first_name = models.CharField(
        verbose_name='First Name',
        max_length=30)

    last_name = models.CharField(
        verbose_name='Las Name',
        max_length=30)

    position = models.CharField(
        verbose_name='Position',
        max_length=20)

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

    phone_alt = EncryptedCharField(
        verbose_name='Telephone (alternate)',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    email = models.EmailField()

    owner = models.ForeignKey(User, on_delete=PROTECT)

    class Meta:
        verbose_name_plural = 'contacts'

    @property
    def full_name(self):
        return f'{self.first_name}, {self.last_name}'

    def __str__(self):
        return f'{self.full_name}'
