# components/inputs.py

from flask import render_template_string
from ..utils import get_jinja_subtemplate
from ..themes import THEME_COLORS
from ..theme_utils import get_global_theme

class BaseInput:
    """
    Base class for creating input components for a dashboard.
    """
    def __init__(self, name: str, default_value: str = ""):
        """
        Initialize a new instance of the BaseInput.

        Args:
            name (str): Name of the input component.
            default_value (str, optional): Default value of the input component. 
            Defaults to an empty string.
        """
        self.name = name
        self.default_value = default_value
        self.theme_colors = THEME_COLORS[get_global_theme()]

    def capture(self, request):
        """
        Capture input value from a web request.

        Args:
            request: Web request object from Flask.
        """
        self.value = request.form.get(self.name, self.default_value)

class InputDropdown(BaseInput):
    """
    A class representing a dropdown input component for a dashboard.
    """
    def __init__(self, name, label, values, action_url="/", 
                 selected_value="Select All"): 
        """
        Initialize a new instance of InputDropdown.

        Args:
            name (str): Name of the dropdown component.
            label (str): Display label for the dropdown.
            values: Either a list of dropdown values or a tuple containing a DataFrame 
            and column name.
            action_url (str, optional): URL to which the form submits. Defaults to "/".
            selected_value (str, optional): Initially selected value in the dropdown. 
            Defaults to "Select All".

        Raises:
            ValueError: If the provided values are neither a list nor a tuple of 
            DataFrame and column name.

        >>> Example of using a dropdown input component within the create_input_group 
        method:

            input_group = ComponentManager.create_input_group(
                manager_instance=index_manager,
                inputs=[
                    {
                        'type': 'dropdown',
                        'name': 'condition_selection',
                        'label': 'Select a condition:',
                        'values': (df, 'condition')
                    }
                ]
            )

        """
        super().__init__(name, selected_value)
        
        self.label = label
        if isinstance(values, tuple) and len(values) == 2 and hasattr(values[0], 'loc'):
            self.values = ["Select All"] + values[0][values[1]].unique().tolist()
        elif isinstance(values, list):
            self.values = ["Select All"] + values
        else:
            raise ValueError("""Invalid values provided. It should be either 
                             a list or a tuple with DataFrame and column name.""")
        
        self.action_url = action_url
        self.selected_value = selected_value

    def capture(self, request):
        """
        Capture selected value from a web request.

        Args:
            request: Web request object from Flask.
        """
        self.value = request.form.get(self.name)
        
        if not self.value:
            self.value = "Select All"

        self.selected_value = self.value

    def render(self):
        """
        Render the dropdown component as an HTML string.

        Returns:
            str: HTML representation of the dropdown component.
        """
        return render_template_string(
            get_jinja_subtemplate("inputs/inputdropdown.j2"), 
            name=self.name, 
            label=self.label, 
            values=self.values, 
            selected_value=self.selected_value,
            theme_colors=self.theme_colors)
    
class TextInput(BaseInput):
    """
    Represents a text input component for a dashboard.
    """
    def __init__(self, name, label, default_value=""):
        """
        Initialize a new instance of the TextInput class.

        Args:
            name (str): Name of the text input component.
            label (str): Display label for the text input.
            default_value (str, optional): Default value for the text input. Defaults 
            to an empty string.
        """
        super().__init__(name, default_value)
        self.label = label

    def capture(self, request):
        """
        Capture text value from a web request.

        Args:
            request: Web request object from Flask.
        """
        self.value = request.form.get(self.name, self.default_value)
        self.default_value = self.value

    def render(self):
        """
        Render the text input component as an HTML string.

        Returns:
            str: HTML representation of the text input component.
        """
        return render_template_string(
            get_jinja_subtemplate("inputs/textinput.j2"),
            name=self.name, label=self.label, 
            default_value=self.default_value,
            theme_colors=self.theme_colors)

class InputSlider_Numerical(BaseInput):
    """
    Represents a numerical slider input component for a dashboard.
    """
    def __init__(self, name, label, min_value=0, 
                 max_value=100, step=1, default_value=50):
        """
        Initialize a new instance of the InputSlider_Numerical class.

        Args:
            name (str): Name of the slider input component.
            label (str): Display label for the slider input.
            min_value (int, optional): Minimum value for the slider. Defaults to 0.
            max_value (int, optional): Maximum value for the slider. Defaults to 100.
            step (int, optional): Step increment for the slider. Defaults to 1.
            default_value (int, optional): Default value for the slider. Defaults to 50.
        """
        # Initialize the base attributes
        super().__init__(name, default_value)

        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

    def capture(self, request):
        """
        Capture the selected value from a web request.

        Args:
            request: Web request object from Flask.
        """
        self.value = int(request.form.get(self.name, self.default_value))
        self.default_value = self.value

    def render(self):
        """
        Render the numerical slider input component as an HTML string.

        Returns:
            str: HTML representation of the numerical slider input component.
        """
        return render_template_string(
            get_jinja_subtemplate("inputs/inputslider_numerical.j2"),
            name=self.name, label=self.label, 
            min_value=self.min_value, max_value=self.max_value, step=self.step, 
            default_value=self.default_value, theme_colors=self.theme_colors)

class InputSlider_Categorical(BaseInput):
    """
    Represents a categorical slider input component for a dashboard.
    """
    def __init__(self, name, label, categories, default_value=None):
        """
        Initialize a new instance of the InputSlider_Categorical class.

        Args:
            name (str): Name of the slider input component.
            label (str): Display label for the slider input.
            categories (list): List of categories for the slider. 
            default_value (str, optional): Default category for the slider. If not 
            provided, the first category will be chosen. Defaults to None.
        """
        
        # Ensure the "Select All" is the first option only
        self.categories = ["Select All"] + [cat for cat in categories 
                                            if cat != "Select All"]
        
        # The default value would be the first category if not provided
        super().__init__(name, default_value if default_value else self.categories[0])
        
        self.label = label

    def capture(self, request):
        """
        Capture the selected category from a web request.

        Args:
            request: Web request object from Flask.
        """
        self.value = request.form.get(self.name, self.default_value)
        # Update the default_value to the captured value for rendering purposes
        self.default_value = self.value

    def render(self):
        """
        Render the categorical slider input component as an HTML string.

        Returns:
            str: HTML representation of the categorical slider input component.
        """
        # Position is zero-indexed based on categories list
        default_position = self.categories.index(self.default_value)
        return render_template_string(
            get_jinja_subtemplate("inputs/inputslider_categorical.j2"),
            name=self.name, label=self.label, max_position=len(self.categories)-1, 
            default_position=default_position, categories=self.categories,
            theme_colors=self.theme_colors)


class InputRadio(BaseInput):
    """
    Represents a radio button input component for a dashboard.
    """
    def __init__(self, name, label, options, default_value=None):
        """
        Initialize a new instance of the InputRadio class.

        Args:
            name (str): Name of the radio button input component.
            label (str): Display label for the radio button input.
            options (list): List of options for the radio button.
            default_value (str, optional): Default option for the radio button. If not 
            provided, the first option will be chosen. Defaults to None.

        Note:
            The option "Select All" will always be the first option if it's not already 
            in the provided list.
        """
        # Ensure 'Select All' is the first option in the list
        if "Select All" not in options:
            options.insert(0, "Select All")

        # If no default_value is provided, set it to the first option
        super().__init__(name, default_value if default_value else options[0])

        self.label = label
        self.options = options

    def capture(self, request):
        """
        Capture the selected option from a web request.

        Args:
            request: Web request object from Flask.
        """
        captured_value = request.form.get(self.name)
        if not captured_value:
            # If no value is captured (i.e., no radio button was clicked),
            # keep the default_value unchanged.
            self.value = self.default_value
        else:
            self.value = captured_value
            # Update the default_value to the captured value for rendering purposes
            self.default_value = captured_value

    def render(self):
        """
        Render the radio button input component as an HTML string.

        Returns:
            str: HTML representation of the radio button input component.
        """
        return render_template_string(
            get_jinja_subtemplate("inputs/inputradio.j2"),
            name=self.name, label=self.label, options=self.options, 
            default_value=self.default_value, theme_colors=self.theme_colors)
