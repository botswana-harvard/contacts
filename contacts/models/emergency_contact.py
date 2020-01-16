from django.db import models
from django.utils.translation import gettext_lazy as _


from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_mixins import BaseUuidModel


class EmergencyContact(BaseUuidModel):

    contact_category = models.CharField(_('Contact Category'), max_length=100)
    
    contact_name = models.CharField(_('Contact name'), max_length=150)
    
    email = models.EmailField(_('email address'), blank=True)
    
    position = models.CharField(
        verbose_name='Position',
        max_length=250)

    contact_number = EncryptedCharField(
        verbose_name='Contact number',
        null=False,
        help_text='')

    contact_number_alt = EncryptedCharField(
        verbose_name='Cell (alternate)',
        blank=True,
        null=True)

    class Meta:
        verbose_name_plural = 'Emergency Contacts'



    def __str__(self):
        return f'{self.contact_category} {self.contact_number}'
