from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    audit_fieldset_tuple, ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)

from ..admin_site import contact_admin
from ..forms import ContactForm
from ..models import Contact, Department


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


@admin.register(Contact, site=contact_admin)
class ContactAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ContactForm

    search_fields = ['first_name', 'last_name', 'email', 'cell', 'phone']

    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'department',
                'position',
                'cell',
                'cell_alt',
                'phone',
                'phone_extension',
                'phone_alt',)},
         ),
        audit_fieldset_tuple
    )
    list_display = (
        'first_name', 'last_name', 'email', 'cell', 'phone')



@admin.register(Department, site=contact_admin)
class DepartmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ContactForm

    search_fields = ['name']

    fieldsets = (
        (None, {
            'fields': (
                'name',)},
         ),
        audit_fieldset_tuple
    )
    list_display = (
        'name',)
