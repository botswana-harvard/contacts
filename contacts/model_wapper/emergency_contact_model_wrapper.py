from edc_model_wrapper.wrappers import ModelWrapper


class EmergencyContactModelWrapper(ModelWrapper):

    model = 'contacts.emergencycontact'
    next_url_name = 'home_url'
    