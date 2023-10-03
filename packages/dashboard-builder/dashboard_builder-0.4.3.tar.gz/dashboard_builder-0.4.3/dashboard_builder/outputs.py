import os
from flask import render_template_string


class TemplateManager:
    
    templates = os.listdir(os.path.join(os.path.dirname(__file__), 'dashboard_templates')) # noqa
    templates_dict = {os.path.splitext(template)[0]: template for template in templates}
    
    @staticmethod
    def dashboard_template(template_name: str) -> str:
        """
        Retrieves a dashboard template from the dashboard builder templates directory.
        ... (rest of the docstring) ...
        """
        current_dir = os.path.dirname(__file__) 
        file_name = TemplateManager.templates_dict.get(template_name, template_name)
        template_path = os.path.join(current_dir, 'dashboard_templates', file_name)
        
        with open(template_path, 'r') as file:
            return file.read()

    @staticmethod
    def dashboard_template_custom(template_name_with_extension: str, template_path: str): # noqa
        """
        Retrieves a custom dashboard template from a user-defined templates directory.
        ... (rest of the docstring) ...
        """
        template_path = os.path.join(template_path, template_name_with_extension)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_name_with_extension}' not found in the directory '{template_path}'") # noqa
        
        with open(template_path, 'r') as file:
            return file.read()


class DashboardOutput:
    
    def __init__(self, manager=None, template_name=None, template_path=None, **kwargs):  # noqa
        
        if manager is None:
            raise ValueError("Manager instance is required.")
        
        # Check for custom template parameters
        if bool(template_path) ^ bool(template_name):  # using XOR to ensure both or neither are provided # noqa
            raise ValueError("Both template_name and template_path must be provided for custom templates.")  # noqa

        self.use_custom_template = bool(template_path) and bool(template_name)

        self.use_custom_template = bool(template_path) and bool(template_name)
        self.template_path = template_path if self.use_custom_template else None
        self.template_name = template_name if self.use_custom_template else 'base'
        self.template_defaults = manager.template_defaults_values
        self.inputs = manager.render_form_groups()
        self.outputs = manager.render_outputs()
        self.custom_params = kwargs
        
    def render(self):
        
        # Decide on which template fetching method to use based on the use_custom_template flag # noqa
        if self.use_custom_template:
            dashboard_template = TemplateManager.dashboard_template_custom(self.template_name, self.template_path) # noqa
        else:
            dashboard_template = TemplateManager.dashboard_template(self.template_name)
        
        # Default context
        dashboard_context = {
            'defaults': self.template_defaults,
            'form_groups': self.inputs,
            'output_components': self.outputs
        }
        
        # Merge with custom parameters
        dashboard_context.update(self.custom_params)
        
        return render_template_string(dashboard_template, **dashboard_context)


