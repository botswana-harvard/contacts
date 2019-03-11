from django.db.models import Q
from django.views.generic import TemplateView, FormView 

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..forms import ContactSearchForm
from ..model_wapper import ContactModelWrapper
from ..models import Contact


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

    def contacts(self, search_value=None):
        """Return contacts.
        """
        contacts = None
        if search_value:
            contacts = Contact.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
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
