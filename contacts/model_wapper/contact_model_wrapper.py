from edc_model_wrapper.wrappers import ModelWrapper


class ContactModelWrapper(ModelWrapper):

    model = 'contacts.contact'
    next_url_name = 'home_url'
    
    @property
    def department(self):
        return self.object.department.name