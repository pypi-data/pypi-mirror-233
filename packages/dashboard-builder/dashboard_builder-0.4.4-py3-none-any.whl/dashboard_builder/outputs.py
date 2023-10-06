import os
from flask import render_template_string

from .theme_utils import get_global_theme
from .themes import THEME_COLORS

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
        
        # Check for default template names
        default_template_names = ['base', 'base_nosidebar']
        
        # Ensure correct parameters are passed based on the template name
        if template_name in default_template_names:
            if template_path:
                raise ValueError("template_path must not be provided for default templates.") # noqa
            self.use_custom_template = False
            self.template_name = template_name
            self.template_path = None
        elif template_name and template_path:
            self.use_custom_template = True
            self.template_name = template_name
            self.template_path = template_path
        elif template_name and not template_path:
            raise ValueError("template_path must be provided if a custom template_name is given.") # noqa
        else:
            self.use_custom_template = False
            self.template_name = 'base'
            self.template_path = None
        
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

        theme_colors = THEME_COLORS[get_global_theme()]

        # Default context
        dashboard_context = {
            'defaults': self.template_defaults,
            'form_groups': self.inputs,
            'output_components': self.outputs,
            'theme_colors': theme_colors,
        }
        
        # Merge with custom parameters
        dashboard_context.update(self.custom_params)
        
        return render_template_string(dashboard_template, **dashboard_context)


