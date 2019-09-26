from django.db.models import Q
from django.views.generic import TemplateView, FormView 

from edc_navbar import NavbarViewMixin

from ..forms import ContactSearchForm
from ..model_wapper import ContactModelWrapper
from ..models import Contact

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.views.generic.base import ContextMixin
from django_revision.views import RevisionMixin


class EdcBaseViewMixin(RevisionMixin, ContextMixin):
    """Mixes in common template variables for the footer, etc.
    """

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        app_config = django_apps.get_app_config('edc_base')
        edc_device_app_config = django_apps.get_app_config('edc_device')
        context = super().get_context_data(**kwargs)
        try:
            live_system = settings.LIVE_SYSTEM
        except AttributeError:
            live_system = None
        context.update({
            'DEBUG': settings.DEBUG,
            'copyright': app_config.copyright,
            'device_id': edc_device_app_config.device_id,
            'device_role': edc_device_app_config.device_role,
            'disclaimer': app_config.disclaimer,
            'institution': app_config.institution,
            'license': app_config.license,
            'project_name': app_config.project_name,
            'live_system': live_system})
        if settings.DEBUG:
            messages.add_message(
                self.request, messages.ERROR,
                ('This EDC is running in DEBUG-mode. Use for testing only. '
                 'Do not use this system for production data collection!'))
        elif not settings.DEBUG and not live_system:
            messages.add_message(
                self.request, messages.WARNING,
                ('This EDC is for testing only. '
                 'Do not use this system for production data collection!'))
        try:
            if settings.WARNING_MESSAGE:
                messages.add_message(
                    self.request, messages.WARNING, settings.WARNING_MESSAGE,
                    extra_tags='warning')
        except AttributeError:
            pass
        return context




class HomeView(
        EdcBaseViewMixin, NavbarViewMixin, FormView, TemplateView):

    form_class = ContactSearchForm
    template_name = 'contacts/home.html'
    navbar_name = 'contacts'
    navbar_selected_item = 'home'
    model_wrapper_cls = ContactModelWrapper

    def form_valid(self, form):
        if form.is_valid():
            search_value = form.cleaned_data['search_value']
            context = self.get_context_data(**self.kwargs)
            context.update(contacts=self.contacts(
                search_value=search_value))
        return self.render_to_response(context)

    @property
    def new_contact(self):
        """Adding a new contact.
        """
        return ContactModelWrapper(Contact())

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def contacts(self, search_value=None):
        """Return contacts.
        """
        contacts = None
        if search_value:
            contacts = Contact.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(cell__icontains=search_value) |
                Q(phone__icontains=search_value))
        else:
            contacts = Contact.objects.all()
        return contacts


    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        wrapped_queryset = self.get_wrapped_queryset(self.contacts())
        context.update({
            'contacts': wrapped_queryset,
            'new_contact': self.new_contact})
        return context

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        object_list = []
        for obj in queryset:
            object_list.append(self.model_wrapper_cls(obj))
        return object_list
