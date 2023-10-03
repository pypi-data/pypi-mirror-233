# components/managers.py

# Third-party imports
from flask import render_template_string
from markdown import markdown

# Local imports
from .components.inputs import (
    InputDropdown,
    InputSlider_Numerical,
    InputSlider_Categorical,
    InputRadio,
    TextInput
)

from .components.outputs import (
    OutputText,
    OutputChart_Matplotlib,
    OutputChart_Altair,
    OutputTable_HTML,
    OutputImage,
    OutputMarkdown,
    OutputChart_Plotly,
)

from .utils import get_jinja_subtemplate

class OutputGroup:
    def __init__(self, manager):
        self.manager = manager
        self.outputs = []

    def register(self, output):
        self.manager.register_outputs(output)
        self.outputs.append(output)

    def render(self):
        return [output.render() for output in self.outputs]


class FormGroup:
    """
    Represents a form group that can contain multiple input components 
    and optional markdown content at the top and bottom.
    """
    def __init__(self, action_url='/', markdown_top=None, markdown_bottom=None):
        """
        Initializes a FormGroup with an action URL and optional markdown content.

        Args:
            action_url (str, optional): URL to which the form data should be posted. 
                Defaults to '/'.
            markdown_top (str, optional): Markdown content to be displayed at the 
                top of the section. Defaults to None.
            markdown_bottom (str, optional): Markdown content to be displayed at 
                the bottom of the section. Defaults to None.
        """
        self.action_url = action_url
        self.inputs = []
        self.markdown_top = markdown_top
        self.markdown_bottom = markdown_bottom

    def get_input(self, input_name):
        """Retrieve an input component by its name."""
        for input_component in self.inputs:
            if input_component.name == input_name:
                return input_component
        raise ValueError(f"No input with name {input_name} found in the form group.")

    def add_inputs(self, *input_components):
        """
        Add one or multiple input components to the form group.

        Args:
        - *input_components (BaseInput): The input components to add.

        Returns:
        - None
        """
        for input_component in input_components:
            self.inputs.append(input_component)

class ComponentManager:
    """
    Manages components (inputs, outputs, and layouts) for a dashboard or view.
    This class facilitates registering, updating, and rendering components.
    """

    _registry = {}  # to keep track of available input types


    class Inputs:

        @staticmethod
        def dropdown(name, label, values, action_url="/", selected_value="Select All"):
            return InputDropdown(name, label, values, action_url, selected_value)

        @staticmethod
        def text(name, label, default_value=""):
            return TextInput(name, label, default_value)

        @staticmethod
        def radio(name, label, options, default_value=None):
            return InputRadio(name, label, options, default_value)

        @staticmethod
        def slider_numerical(name, label, min_value=0, max_value=100, step=1, default_value=50): # noqa 
            return InputSlider_Numerical(name, label, min_value, max_value, step, default_value) # noqa 

        @staticmethod
        def slider_categorical(name, label, categories, default_value=None):
            return InputSlider_Categorical(name, label, categories, default_value)


    class Outputs:
        @staticmethod
        def text(content):
            """
            For displaying text. 
            """
            return OutputText(content)
        
        @staticmethod
        def matplotlib(content):
            """
            For displaying a matplotlib object. 
            """
            return OutputChart_Matplotlib(content)
        
        @staticmethod
        def table_html(content):
            """
            For displaying a pandas dataframe in a html table. 
            """
            return OutputTable_HTML(content)
        
        @staticmethod
        def plotly(content):
            """
            For displaying a plotly object. 
            """
            return OutputChart_Plotly(content)
        
        @staticmethod
        def altair(content):
            """
            For displaying an altair object. 
            """
            return OutputChart_Altair(content)
        
        @staticmethod
        def markdown(content):
            """
            For displaying markdown. 
            """
            return OutputMarkdown(content)
        

    # Class methods 
    @classmethod
    def register_component(cls, component_type, component_class):
        """Register an input component type with the manager."""
        cls._registry[component_type] = component_class

    @classmethod
    def create_component(cls, component_type, *args, **kwargs):
        """Factory method to create and return an instance of an input component."""
        if component_type not in cls._registry:
            raise ValueError(f"No component type {component_type} registered.")
        
        component_class = cls._registry[component_type]
        return component_class(*args, **kwargs)

    @classmethod
    def create_input_group(cls, manager_instance, inputs=[], 
                       markdown_top="", markdown_bottom="", action_url=None): # noqa
        """
        ## Creates a input group
        Creates a form group with multiple input components and registers
        the form group and its inputs with the manager instance.

        ## Args
        - `manager_instance` (ComponentManager): An instance of ComponentManager 
            to register inputs and form groups. This is the manager instance
            that will be used to render the dashboard for this endpoint. 
        - `action_url` (str): The URL the form should post to. Defaults to the
            default route of the manager instance. Which is the URL of the current
            request.
        - `markdown_top` (str): Markdown content to display at the top 
            of the form group. Optional. 
        - `markdown_bottom` (str): Markdown content to display at the bottom of the 
            form group. Optional. 
        - `inputs` (list): List of input components from ComponentManager.Inputs 

        ## Returns
        - FormGroup: The created FormGroup instance.

        ## Example
        >>>     form_group = ComponentManager.create_input_group(
                    manager_instance=manager,
                    action_url='/',
                    markdown_top='',
                    markdown_bottom='',
                    inputs=[]
                )
        """
        if action_url is None:
            action_url = manager_instance.default_route

        form_group = FormGroup(action_url=action_url, markdown_top=markdown_top, markdown_bottom=markdown_bottom) # noqa
        
        # Add inputs to the form group
        for input_component in inputs:
            form_group.add_inputs(input_component)
            manager_instance.register_inputs(input_component)

        # Register the form group
        manager_instance.register_form_groups(form_group)
        
        return form_group


    @staticmethod
    def create_output_group(manager_instance, outputs):
        """
        Creates an output group. This can have multiple output components, and it 
        registers the output group and its outputs with the manager instance.

        ## Args
        - `manager_instance` (ComponentManager): An instance of ComponentManager 
            to register outputs and output groups. This is the manager instance
            that will be used to render the dashboard for this endpoint.
        - `outputs` (list): List of output components from ComponentManager.Outputs 

        """
        output_group = OutputGroup(manager_instance)
        for output_component in outputs:
            output_group.register(output_component)
        return output_group

    
    # Initialization
    def __init__(self, request):
        """
        Initialize the ComponentManager with a request object to handle 
        input components.
        
        Args:
            request (flask.Request): The current Flask request object. Which is 
                dedicated by the current request endpoint. Set by @app.route(...) 

        """
        self.request = request
        self.default_route = str(self.request.url_rule)
        self.inputs = []
        self.form_groups = []   # list to store registered form groups
        self.outputs = []
        self.layouts = []
        self._template_defaults = {
            "footer_text": "Powered by Dashboard Builder"
        }

    # Instance methods
    def register_inputs(self, *input_components):
        """
        Register multiple input components, capture their values from the request, 
        and append them to the inputs list.

        Args:
        - *input_components (BaseInput): The input components to register.

        Returns:
        - list: List of registered input components.
        """
        for input_component in input_components:
            input_component.capture(self.request)
            self.inputs.append(input_component)
        return self.inputs
    
    def register_form_groups(self, *form_groups):
        """
        Register multiple form groups and append them to the form_groups list.
        
        Args:
        - *form_groups (FormGroupManager): The form groups to register.

        Returns:
        - list: List of registered form groups.
        """
        for form_group in form_groups:
            self.form_groups.append(form_group)
        return self.form_groups
    
    def register_output(self, output_component):
        """
        Register an output component and append it to the outputs list.
        
        Args:
        - output_component (BaseOutput): The output component to register.

        Returns:
        - BaseOutput: The registered output component.
        """
        self.outputs.append(output_component)
        return output_component
    
    def register_outputs(self, *output_components):
        """
        Register multiple output components and append them to the outputs list.
        
        Args:
        - *output_components (BaseOutput): The output components to register.

        Returns:
        - list: List of registered output components.
        """
        for output_component in output_components:
            self.outputs.append(output_component)
        return self.outputs
    
    def register_layouts(self, *layouts):
        """Register one or more layouts.

        Args:
        - *layouts (ColumnLayout): The layouts to register.

        Returns:
        - list: List of registered layouts.
        """
        for layout in layouts:
            self.outputs.append(layout)
        return layouts
    
    def render_inputs(self):
        """
        Render all the registered input components.
        
        Returns:
        - list: List of rendered input components.
        """
        return [input_component.render() for input_component in self.inputs]
    
    def render_form_groups(self):
        """
        Render each form group in the form_groups list as an HTML string.
        
        For each form group, the method:
        1. Renders its input components.
        2. Converts markdown content to HTML.
        3. Renders the entire form group with the provided from the form group template.

        Returns:
        - list: List of rendered HTML strings for each form group.
        """
        rendered_form_groups = []
        for form_group in self.form_groups:
            inputs = [input_component.render() for input_component in form_group.inputs]
            rendered_form_group = render_template_string(
                get_jinja_subtemplate("formgroups/formgroup.j2"), 
                action_url=form_group.action_url, 
                inputs=inputs,
                markdown_top=markdown(form_group.markdown_top),
                markdown_bottom=markdown(form_group.markdown_bottom)
            )
            rendered_form_groups.append(rendered_form_group)
        return rendered_form_groups
    
    def render_outputs(self):
        """
        Render all the registered output components.
        
        Returns:
        - list: List of rendered output components.
        """
        return [output_component.render() for output_component in self.outputs]
    
    def render_layouts(self):
        """Render all registered layouts."""
        return [layout.render() for layout in self.layouts]

    def template_defaults(self, **kwargs):
        """
        Update the manager's configuration with provided keyword arguments.
        """
        self._template_defaults.update(kwargs)

    @property
    def template_defaults_values(self):
        """
        Return the current configuration values.
        """
        return self._template_defaults


# Registering input components
ComponentManager.register_component('dropdown', InputDropdown)
ComponentManager.register_component('intput_text', TextInput)
ComponentManager.register_component('slider_numerical', InputSlider_Numerical)
ComponentManager.register_component('slider_categorical', InputSlider_Categorical)
ComponentManager.register_component('radio', InputRadio)

# Registering output components
ComponentManager.register_component('text', OutputText)
ComponentManager.register_component('chart_matplotlib', OutputChart_Matplotlib)
ComponentManager.register_component('chart_plotly', OutputChart_Plotly)
ComponentManager.register_component('chart_altair', OutputChart_Altair)
ComponentManager.register_component('table_html', OutputTable_HTML)
ComponentManager.register_component('image', OutputImage)
ComponentManager.register_component('markdown', OutputMarkdown)


