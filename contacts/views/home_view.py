from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..models import Contact


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'contacts/home.html'
    navbar_name = 'contacts'
    navbar_selected_item = 'home'

    @property
    def contacts(self):
        """Return contacts.
        """
        return Contact.objects.all()


    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context.update({
            'contacts': self.contacts})
        return context